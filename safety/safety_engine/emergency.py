"""응급 흐름(5-4) 상태 기계.

중단 → "괜찮으세요?" → (아니에요 | 무응답) → 보호자 알림
심한 증상 → 119 화면(발신은 1탭 확인) → 무응답이면 보호자에게 119 연결 요청
"""
from enum import Enum

from .codes import Code


class EmState(str, Enum):
    ASK_OK = "ASK_OK"
    RESTING_OK = "RESTING_OK"                # 끝: 괜찮다고 답함
    GUARDIAN_ALERTED = "GUARDIAN_ALERTED"    # 끝: 보호자에게 전화+푸시
    SHOW_119 = "SHOW_119"
    CALLING_119 = "CALLING_119"              # 끝: 사용자가 119 발신 확인
    GUARDIAN_119 = "GUARDIAN_119"            # 끝: 보호자에게 119 연결 요청


class EmAction(str, Enum):
    REST_GUIDANCE = "REST_GUIDANCE"          # 앉아서 쉬세요 음성
    ASK_OK = "ASK_OK"                        # 괜찮아요 / 아니에요 큰 버튼 2개
    SHOW_119 = "SHOW_119"
    DIAL_119 = "DIAL_119"
    NOTIFY_GUARDIAN = "NOTIFY_GUARDIAN"      # 전화 우선, 앱 푸시 병행
    GUARDIAN_CALL_119 = "GUARDIAN_CALL_119"  # 보호자에게 119 연결 요청


TERMINAL = {EmState.RESTING_OK, EmState.GUARDIAN_ALERTED, EmState.CALLING_119, EmState.GUARDIAN_119}


class EmergencyFlow:
    def __init__(self, rules, t, severe, snapshot=None):
        """snapshot: 마지막 혈압·심박 등 보호자·응급 시 전달할 사건 정보(위치는 별도 동의 시에만)."""
        self.e = rules["emergency"]
        self.snapshot = snapshot or {}
        self.now = t
        self.state = None
        self.deadline = None
        self.started = self._show_119(t, Code.EM_SEVERE_SYMPTOM) if severe else self._ask_ok(t)

    def _ask_ok(self, t):
        self.state = EmState.ASK_OK
        self.deadline = t + self.e["ask_ok_timeout_seconds"]
        return [(EmAction.REST_GUIDANCE, None), (EmAction.ASK_OK, None)]

    def _show_119(self, t, code):
        self.state = EmState.SHOW_119
        self.deadline = t + self.e["call_119_confirm_timeout_seconds"]
        return [(EmAction.SHOW_119, code)]

    def _advance(self, t):
        if t < self.now:
            raise ValueError("time went backwards")
        self.now = t
        return self.state not in TERMINAL

    def answer(self, t, ok):
        if not self._advance(t) or self.state != EmState.ASK_OK:
            return []
        if ok:
            self.state = EmState.RESTING_OK
            return [(EmAction.REST_GUIDANCE, Code.EM_USER_OK)]
        self.state = EmState.GUARDIAN_ALERTED
        return [(EmAction.NOTIFY_GUARDIAN, Code.EM_USER_NOT_OK)]

    def report_severe(self, t):
        """"괜찮으세요?" 단계에서 흉통·실신감·마비 등이 새로 보고됨 → 119로 올린다."""
        if not self._advance(t) or self.state != EmState.ASK_OK:
            return []
        return self._show_119(t, Code.EM_SEVERE_SYMPTOM)

    def confirm_119(self, t):
        if not self._advance(t) or self.state != EmState.SHOW_119:
            return []
        self.state = EmState.CALLING_119
        return [(EmAction.DIAL_119, Code.EM_119_CONFIRMED), (EmAction.NOTIFY_GUARDIAN, Code.EM_119_CONFIRMED)]

    def tick(self, t):
        if not self._advance(t) or t < self.deadline:
            return []
        if self.state == EmState.ASK_OK:
            self.state = EmState.GUARDIAN_ALERTED
            return [(EmAction.NOTIFY_GUARDIAN, Code.EM_NO_RESPONSE)]
        if self.state == EmState.SHOW_119:
            self.state = EmState.GUARDIAN_119
            return [(EmAction.GUARDIAN_CALL_119, Code.EM_119_NO_CONFIRM)]
        return []
