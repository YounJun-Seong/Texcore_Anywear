"""앱·서버가 쓰는 진입점. 모든 판정을 판정 로그에 남긴다."""
from . import precheck
from .codes import Light
from .emergency import EmergencyFlow
from .rules import load_rules
from .session import SessionMonitor, hr_limits


class SafetyEngine:
    def __init__(self, rules=None, log=None):
        self.rules = rules or load_rules()
        self.log = log

    def record(self, kind, payload):
        """판정 외 사건(단말 운동 기록·응급 보고)도 같은 로그 체인에 남긴다."""
        if self.log is not None:
            self.log.append(kind, payload, self.rules.version, self.rules.sha256)

    def _logged(self, decision):
        self.record(decision.kind, decision.to_dict())
        return decision

    def hard_gate(self, profile):
        return self._logged(precheck.hard_gate(self.rules, profile))

    def pre_check(self, profile, vitals, symptoms=(), conditions=()):
        return self._logged(precheck.pre_check(self.rules, profile, vitals, symptoms, conditions))

    def post_check(self, resting_hr, hr_after_recovery):
        return self._logged(precheck.post_check(self.rules, resting_hr, hr_after_recovery))

    def allowance(self, light, planned_minutes):
        return precheck.allowance(self.rules, light, planned_minutes)

    def start_session(self, profile, hr_grade, light=Light.GREEN, weeks_since_start=0,
                      escalation_approved=False, start_t=0.0):
        limits = hr_limits(self.rules, profile, weeks_since_start, escalation_approved, light)
        self.record("session_start", {"limits": limits, "hr_grade": hr_grade, "light": Light(light).value})
        monitor = SessionMonitor(self.rules, limits["ceiling"], hr_grade, start_t,
                                 sink=lambda rec: self.record("session_event", rec))
        return limits, monitor

    def start_emergency(self, t, severe, snapshot=None):
        flow = EmergencyFlow(self.rules, t, severe, snapshot)
        self.record("emergency_start", {"t": t, "severe": severe, "snapshot": flow.snapshot,
                                         "actions": [(a.value, c) for a, c in flow.started]})
        return flow
