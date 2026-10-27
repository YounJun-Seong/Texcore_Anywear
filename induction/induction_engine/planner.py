"""오늘의 계획(6-7 plan_today).

안전 엔진이 먼저 판정하고, 유도 엔진은 그 결과를 바꿀 수 없다.
분·강도는 언제나 안전 엔진 allowance() 상한 이하로만 나온다.
"""
from safety_engine.precheck import allowance

from .activity import easier_activity, pick_activity, weather_reason
from .history import completed
from .ladder import minutes_budget, step_minutes
from .messages import pick_message
from .state import classify_state
from .types import Plan, UserState


def _msg(cfg, intent, history, today, values=None):
    return pick_message(cfg, intent, history.messages, today, values)[0]


def plan_today(cfg, safety_rules, profile, ladder, history, decision, today, weather=None):
    """
    decision: 안전 엔진 pre_check 결과(오늘 혈압·증상 입력 직후 = 앵커 순간, R17)
    ladder: 오늘 ladder_update()를 거친 상태
    """
    light = decision.outcome

    # R02: 안전 엔진이 운동을 막은 경우 그대로 전달
    if light == "EMERGENCY":
        return Plan(action="EMERGENCY", light=light, notify_guardian=True, rules_fired=("R02",))
    if light == "BLOCKED":
        return Plan(action="DOCTOR_CHECK", light=light, message=_msg(cfg, "doctor_check", history, today),
                    rules_fired=("R02",))
    if light == "REMEASURE":
        return Plan(action="REMEASURE", light=light, message=_msg(cfg, "remeasure", history, today),
                    rules_fired=("R02",))

    state = classify_state(cfg, history.sessions, profile.signup_date, today)
    base = dict(light=light, state=state.value, level=ladder.level)

    # R01·R16: 빨강 → 쉬기, 쉰 것도 칭찬(도장)
    if light == "RED":
        return Plan(action="REST_AND_PRAISE", message=_msg(cfg, "rest_red", history, today),
                    rules_fired=("R01", "R16"), detail={"stamp": True}, **base)
    if light not in ("GREEN", "YELLOW"):
        raise ValueError(f"unknown safety outcome {light}")

    rules = []
    step = step_minutes(cfg, ladder.level)
    allowed = allowance(safety_rules, light, step)
    if light == "YELLOW":
        rules.append("R03")
    budget = minutes_budget(cfg, ladder.level, history, today)
    minutes = min(step, allowed["max_minutes"], budget["minutes"])
    if budget["minutes"] < min(step, allowed["max_minutes"]):
        rules.append("R07" if budget["binding"] == "daily" else "R08")
    if minutes < cfg["ladder"]["steps_minutes"][0]:
        return Plan(action="DONE_FOR_TODAY", message=_msg(cfg, "done_for_today", history, today),
                    rules_fired=tuple(rules), detail={"budget": budget}, **base)

    done = sorted(completed(history.sessions, end=today), key=lambda s: s.day)
    slow_recovery = bool(done) and done[-1].slow_recovery
    intensity = "moderate"
    if allowed["intensity"] == "low" or state == UserState.FEAR or slow_recovery:
        intensity = "low"
    if state == UserState.FEAR:
        rules.append("R04")

    wkey = weather_reason(cfg, weather)
    if wkey:
        rules.append("R06")
    activity = pick_activity(cfg, history, today, intensity, state, wkey, profile.fall_concern)
    rules.append("R05")

    easier_minutes = max([s for s in cfg["ladder"]["steps_minutes"] if s < minutes],
                         default=cfg["ladder"]["mini_session_minutes"])
    easier = {"minutes": easier_minutes,
              "activity_id": easier_activity(cfg, activity, wkey, profile.fall_concern)["id"]}

    if wkey:
        intent = "today_weather"
    elif light == "YELLOW":
        intent = "today_yellow"
    else:
        intent = f"today_{state.value}"
    message = _msg(cfg, intent, history, today, {
        "minutes": minutes, "activity": activity["name"], "goal": profile.goal,
        "reason": cfg["weather"]["reasons"].get(wkey) if wkey else None})
    rules.append("R14")
    if profile.anchor == "bp":
        rules.append("R17")

    return Plan(action="EXERCISE", minutes=minutes, activity_id=activity["id"], intensity=intensity,
                easier=easier, message=message, rules_fired=tuple(rules),
                detail={"allowance": allowed, "budget": budget, "weather": wkey, "slow_recovery": slow_recovery},
                **base)


def completion_message(cfg, profile, history, today):
    """완료 직후 칭찬. 목표가 있으면 그 말로(6-5). 운동량과 상관없이 같은 칭찬."""
    if profile.goal:
        return pick_message(cfg, "complete_goal", history.messages, today, {"goal": profile.goal})[0]
    return pick_message(cfg, "complete", history.messages, today)[0]


def ladder_message(cfg, history, today, ladder, code):
    """사다리 변화 안내. 강등은 '실패'가 아니라 다음 운동을 더 안전하게."""
    intent = {"LADDER_UP": "level_up", "LADDER_DOWN_SAFETY": "level_down",
              "LADDER_DOWN_MISSED": "level_down", "LADDER_RESTART": "restart_offer"}.get(code)
    if intent is None:
        return None
    return pick_message(cfg, intent, history.messages, today, {"minutes": step_minutes(cfg, ladder.level)})[0]
