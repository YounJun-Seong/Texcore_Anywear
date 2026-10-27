from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(frozen=True)
class DoctorLimits:
    """의사가 정한 개인 한도. 기본 규칙보다 엄격할 때만 적용된다."""
    systolic_max: Optional[int] = None       # 이 값 이상이면 오늘은 쉬기
    diastolic_max: Optional[int] = None
    resting_hr_max: Optional[int] = None
    exercise_hr_ceiling: Optional[int] = None  # 운동 중 심박 상한(심박조율기·ICD는 필수)


@dataclass(frozen=True)
class Profile:
    age: int
    conditions: frozenset = frozenset()      # hard_gate.conditions_requiring_clearance 중 해당 항목
    parq_risk: bool = False                  # 간소화 PAR-Q+ 위험 응답 여부
    doctor_clearance: bool = False           # 의사 확인서 제출 여부
    device: Optional[str] = None             # pacemaker | icd | None
    beta_blocker: bool = False               # 심박 조절 약 복용
    doctor_limits: DoctorLimits = field(default_factory=DoctorLimits)

    def to_dict(self):
        d = asdict(self)
        d["conditions"] = sorted(self.conditions)
        return d


@dataclass(frozen=True)
class Vitals:
    """운동 전 측정값(앉아서 5분 쉰 뒤). source: manual | ble_upper_arm | chest_strap | watch"""
    systolic: Optional[float] = None
    diastolic: Optional[float] = None
    resting_hr: Optional[float] = None
    bp_source: str = "manual"
    hr_source: str = "manual"


@dataclass(frozen=True)
class Decision:
    kind: str                 # hard_gate | pre_check | post_check
    outcome: str
    reasons: tuple
    rule_version: str
    rule_sha256: str
    inputs: dict
    detail: dict = field(default_factory=dict)

    def to_dict(self):
        d = asdict(self)
        d["reasons"] = list(self.reasons)
        return d
