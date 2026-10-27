from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import Enum
from typing import Optional


class UserState(str, Enum):
    FEAR = "FEAR"              # ① 두려움·무관심
    STARTING = "STARTING"      # ② 시작
    HABIT = "HABIT"            # ③ 습관 형성
    LAPSE_RISK = "LAPSE_RISK"  # ④ 유지·이탈 위험


@dataclass(frozen=True)
class UserProfile:
    signup_date: date
    preferred_time: time = time(9, 0)
    anchor: str = "time"                  # bp(혈압 재기) | time | after_meds | after_drama ...
    goal: Optional[str] = None            # "손주 안아주기" 등. 생성형 AI에는 보내지 않는다.
    fall_concern: bool = False
    guardian_mode: str = "none"           # none | full | cheer_only(응원 버튼만, 운동 여부는 안 보냄)
    consent_guardian_cheer_request: bool = False
    has_guardian_cheer: bool = False      # 녹음된 응원 음성이 있음
    manager_linked: bool = False          # 보건소·복지관 담당자 연결
    consent_manager: bool = False


@dataclass(frozen=True)
class SessionRecord:
    day: date
    completed: bool
    minutes: float
    level: int                            # 그때의 사다리 단계(0부터)
    kind: str
    activity_id: str
    stopped: bool = False                 # 운동 중 STOP·119
    max_rpe: Optional[int] = None
    start_time: Optional[time] = None
    slow_recovery: bool = False           # 안전 엔진 post_check: 다음 강도 낮춤


@dataclass(frozen=True)
class PrecheckRecord:
    day: date
    light: str                            # 안전 엔진 pre_check 결과


@dataclass(frozen=True)
class NotificationRecord:
    sent_at: datetime
    message_id: str
    opened: bool                          # 알림 후 60분 안에 앱을 열었는지


@dataclass(frozen=True)
class MessageUse:
    day: date
    message_id: str


@dataclass(frozen=True)
class History:
    sessions: tuple = ()
    prechecks: tuple = ()
    notifications: tuple = ()
    messages: tuple = ()


@dataclass(frozen=True)
class LadderState:
    level: int
    last_change: date
    restart_pending: bool = False


@dataclass(frozen=True)
class Weather:
    precipitation: bool = False
    temp_c: Optional[float] = None
    pm10: Optional[float] = None
    pm25: Optional[float] = None


@dataclass(frozen=True)
class Message:
    id: str
    intent: str
    text: str


@dataclass(frozen=True)
class Plan:
    action: str                           # EXERCISE | REST_AND_PRAISE | REMEASURE | DOCTOR_CHECK | EMERGENCY | DONE_FOR_TODAY
    light: str
    state: Optional[str] = None
    level: Optional[int] = None
    minutes: int = 0
    activity_id: Optional[str] = None
    intensity: Optional[str] = None
    easier: Optional[dict] = None         # "더 쉬운 걸로" 1개: {minutes, activity_id}
    message: Optional[Message] = None
    notify_guardian: bool = False
    rules_fired: tuple = ()
    detail: dict = field(default_factory=dict)
