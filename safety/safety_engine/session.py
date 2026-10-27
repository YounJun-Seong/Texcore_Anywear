"""운동 중 규칙(5-3).

SessionMonitor는 단말에서 1초 간격 tick과 센서·사용자 이벤트를 받아 행동을 돌려준다.
시간은 호출자가 넘기는 초 단위 값만 쓰므로(시계 직접 조회 없음) 시나리오 재생이 결정론적이다.
"""
import math
from collections import deque
from dataclasses import dataclass, field

from .codes import ActionKind, Code, Light
from .types import Profile


def _floor(x):
    return math.floor(round(x, 6))


def hr_limits(rules, profile: Profile, weeks_since_start=0, escalation_approved=False, light=Light.GREEN):
    """오늘 세션의 심박 상한·목표 구간."""
    s = rules["session"]
    cp = s["ceiling_pct"]
    max_hr = s["max_hr"]["intercept"] - s["max_hr"]["age_coef"] * profile.age

    if profile.beta_blocker:
        # 심박이 잘 오르지 않으므로 구간 안내는 끄고, 절대 상한만 이상 감지용으로 둔다.
        pct, mode = cp["absolute_max"], "anomaly_only"
    elif weeks_since_start >= s["initial_period_weeks"] and escalation_approved:
        pct, mode = cp["escalated"], "zone"
    else:
        pct, mode = cp["initial"], "zone"
    pct = min(pct, cp["absolute_max"])

    cap = rules["allowance"].get(Light(light).value, {}).get("hr_ceiling_pct_cap")
    if cap is not None:
        pct = min(pct, cap)

    ceiling = _floor(max_hr * pct)
    doctor = profile.doctor_limits.exercise_hr_ceiling
    if doctor is not None:
        ceiling = min(ceiling, doctor)
    elif profile.device in rules["hard_gate"]["devices_requiring_doctor_hr_ceiling"]:
        raise ValueError("pacemaker/ICD user without doctor HR ceiling must be blocked by the hard gate")

    zone_lower = None if mode == "anomaly_only" else min(math.ceil(round(max_hr * s["zone_pct"]["lower"], 6)), ceiling)
    return {"max_hr": round(max_hr, 1), "ceiling_pct": pct, "ceiling": ceiling,
            "zone_lower": zone_lower, "mode": mode}


@dataclass(frozen=True)
class Action:
    t: float
    kind: ActionKind
    code: str
    detail: dict = field(default_factory=dict)

    def key(self):
        return (self.t, self.kind.value, self.code)


class SessionMonitor:
    def __init__(self, rules, ceiling, hr_grade=None, start_t=0.0, sink=None):
        """
        ceiling: hr_limits()["ceiling"]
        hr_grade: 심박 출처 등급 A | B | C | None(심박 장치 없음, 폰만으로)
        sink: 행동 목록을 받아 판정 로그에 남기는 콜백(선택)
        """
        s = rules["session"]
        self.s = s
        self.ceiling = ceiling
        grade_rule = s["heart_rate_grades"].get(hr_grade) if hr_grade else None
        self.uses_hr = bool(grade_rule and grade_rule["use_hr"])
        self.hr_max_action = ActionKind(grade_rule["max_hr_action"]) if self.uses_hr else None
        self.normal_interval = s["checkin_interval_seconds"] if self.uses_hr else s["no_sensor_checkin_interval_seconds"]
        self.checkin_interval = self.normal_interval
        self.sink = sink

        self.now = start_t
        self.stopped = False
        self.paused = False
        self.over_since = None
        self.slowed_at = None
        self.last_valid_hr_t = start_t
        self.sensor_fallback = False
        self.last_checkin_t = start_t
        self.last_interaction_t = start_t
        self.no_response_alerted = False
        self.recent = deque()

    # ---- 공개 이벤트 ----
    def tick(self, t):
        return self._run(t, "tick", None, lambda out: None)

    def on_hr(self, t, bpm):
        return self._run(t, "hr", bpm, lambda out: self._hr(t, bpm, out), check_gap_first=True)

    def on_rpe(self, t, answer):
        value = self._rpe_value(answer)

        def handle(out):
            self.last_checkin_t = t
            if value >= self.s["rpe"]["stop_at"]:
                self._stop(t, ActionKind.STOP, Code.RPE_VERY_HARD, out, {"rpe": value})
            elif value >= self.s["rpe"]["step_down_at"]:
                out.append(Action(t, ActionKind.STEP_DOWN, Code.RPE_HARD, {"rpe": value}))
        return self._run(t, "rpe", answer, handle, interaction=True)

    def on_symptom(self, t, symptom):
        if symptom in self.s["emergency_symptoms"]:
            kind, code = ActionKind.EMERGENCY_119, Code.EMERGENCY_SYMPTOM
        elif symptom in self.s["stop_symptoms"]:
            kind, code = ActionKind.STOP, Code.STOP_SYMPTOM
        else:
            raise ValueError(f"unknown symptom: {symptom}")
        return self._run(t, "symptom", symptom,
                         lambda out: self._stop(t, kind, code, out, {"symptom": symptom}), interaction=True)

    def on_user_stop(self, t):
        """항상 보이는 "그만" 버튼."""
        return self._run(t, "user_stop", None,
                         lambda out: self._stop(t, ActionKind.STOP, Code.USER_STOP, out), interaction=True)

    def on_interaction(self, t):
        return self._run(t, "interaction", None, lambda out: None, interaction=True)

    def resume(self, t):
        """일시정지 후 사용자가 회복했다고 답하고 다시 시작."""
        def handle(out):
            self.paused = False
            self.over_since = None
            self.slowed_at = None
            self.last_checkin_t = t
        return self._run(t, "resume", None, handle, interaction=True)

    # ---- 내부 ----
    def _run(self, t, event, value, handler, interaction=False, check_gap_first=False):
        if t < self.now:
            raise ValueError(f"time went backwards: {t} < {self.now}")
        self.now = t
        if self.stopped:
            return []
        out = []
        if interaction:
            self.last_interaction_t = t
            self.no_response_alerted = False
        if check_gap_first:
            self._check_gap(t, out)
        handler(out)
        if not self.stopped:
            self._time_checks(t, out)
        if out and self.sink:
            self.sink({"t": t, "event": event, "value": value,
                       "actions": [{"kind": a.kind.value, "code": a.code, "detail": a.detail} for a in out]})
        return out

    def _rpe_value(self, answer):
        r = self.s["rpe"]
        value = r["answer_map"][answer] if isinstance(answer, str) else answer
        if not (r["valid"]["min"] <= value <= r["valid"]["max"]):
            raise ValueError(f"RPE out of range: {answer}")
        return value

    def _stop(self, t, kind, code, out, detail=None):
        self.stopped = True
        out.append(Action(t, kind, code, detail or {}))

    def _hr_alarm(self, t, code, out, detail):
        """심박 기반 중단 신호. B 등급 센서는 일시정지까지만 올린다."""
        if self.hr_max_action == ActionKind.STOP:
            self._stop(t, ActionKind.STOP, code, out, detail)
        elif not self.paused:
            self.paused = True
            out.append(Action(t, ActionKind.PAUSE, code, detail))

    def _enter_fallback(self, t, code, out):
        if self.sensor_fallback:
            return
        self.sensor_fallback = True
        self.checkin_interval = self.s["sensor"]["fallback_checkin_interval_seconds"]
        self.over_since = None
        self.slowed_at = None
        out.append(Action(t, ActionKind.SENSOR_FALLBACK, code))
        out.append(Action(t, ActionKind.STEP_DOWN, code))

    def _check_gap(self, t, out):
        if self.uses_hr and not self.sensor_fallback and t - self.last_valid_hr_t > self.s["sensor"]["hr_gap_seconds"]:
            self._enter_fallback(t, Code.SENSOR_GAP, out)

    def _hr(self, t, bpm, out):
        if not self.uses_hr:
            return
        p = self.s["sensor"]["plausible"]
        if not (p["min"] <= bpm <= p["max"]):
            self._enter_fallback(t, Code.SENSOR_IMPLAUSIBLE, out)
            return
        self.last_valid_hr_t = t
        if self.sensor_fallback:
            self.sensor_fallback = False
            self.checkin_interval = self.normal_interval
            out.append(Action(t, ActionKind.SENSOR_RESTORED, Code.SENSOR_OK))

        sc = self.s["sudden_change"]
        while self.recent and t - self.recent[0][0] > sc["window_seconds"]:
            self.recent.popleft()
        jump = max((abs(bpm - b) for _, b in self.recent), default=0)
        self.recent.append((t, bpm))

        if bpm >= round(self.ceiling * self.s["stop_ratio_over_ceiling"], 6):
            self._hr_alarm(t, Code.HR_FAR_OVER_CEILING, out, {"bpm": bpm, "ceiling": self.ceiling})
        elif jump >= sc["delta_bpm"]:
            self._hr_alarm(t, Code.HR_SUDDEN_CHANGE, out, {"bpm": bpm, "jump": jump})
        if self.stopped:
            return

        if bpm > self.ceiling:
            if self.over_since is None:
                self.over_since = t
        else:
            self.over_since = None
            self.slowed_at = None

    def _time_checks(self, t, out):
        s = self.s
        self._check_gap(t, out)

        if not self.paused and self.over_since is not None:
            if self.slowed_at is None and t - self.over_since > s["over_ceiling_seconds_to_slow_down"]:
                self.slowed_at = t
                out.append(Action(t, ActionKind.SLOW_DOWN, Code.HR_OVER_CEILING, {"ceiling": self.ceiling}))
            elif self.slowed_at is not None and t - self.slowed_at >= s["recover_seconds_after_slow_down"]:
                self.paused = True
                out.append(Action(t, ActionKind.PAUSE, Code.HR_NOT_RECOVERED, {"ceiling": self.ceiling}))

        if not self.paused and t - self.last_checkin_t >= self.checkin_interval:
            self.last_checkin_t = t
            out.append(Action(t, ActionKind.ASK_RPE, Code.CHECKIN_DUE))

        if not self.no_response_alerted and t - self.last_interaction_t >= s["no_response_seconds"]:
            self.no_response_alerted = True
            out.append(Action(t, ActionKind.GUARDIAN_ALERT, Code.NO_RESPONSE))
            out.append(Action(t, ActionKind.LOUD_PROMPT, Code.NO_RESPONSE))
