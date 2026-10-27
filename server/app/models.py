"""DB 모델.

- 건강 정보(질환·복용약 유형·의사 한도·혈압·심박)는 민감정보: 별도 동의가 있어야 저장한다.
  저장 시 암호화(AES-256)는 DB·디스크 계층(국내 리전 관리형 DB의 저장 암호화)에서 건다.
- 위치는 저장하지 않는다(응급 시 전송만). 음성 녹음도 저장하지 않는다.
- 판정 로그(DecisionLogRow)는 추가 전용: ORM에서 수정·삭제를 막고 해시 체인으로 변조를 찾는다.
"""
from datetime import date, datetime

from sqlalchemy import (JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint,
                        event)
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(16))              # elder | guardian | admin
    phone: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class OtpCode(Base):
    __tablename__ = "otp_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(32), index=True)
    code_hash: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    used: Mapped[bool] = mapped_column(Boolean, default=False)


class ElderProfile(Base):
    __tablename__ = "elder_profiles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    birth_year: Mapped[int] = mapped_column(Integer)
    signup_date: Mapped[date] = mapped_column(Date)
    proxy_setup: Mapped[bool] = mapped_column(Boolean, default=False)  # 보호자·담당자 대리 설정
    # 민감정보(동의 필요): conditions, parq_risk, doctor_clearance, device, beta_blocker, doctor_limits
    health: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    hr_escalation_approved: Mapped[bool] = mapped_column(Boolean, default=False)  # 4주 후 76% 승급(의료진 확인)
    # 유도 엔진 설정
    preferred_time: Mapped[str] = mapped_column(String(5), default="09:00")
    anchor: Mapped[str] = mapped_column(String(32), default="time")
    goal: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fall_concern: Mapped[bool] = mapped_column(Boolean, default=False)
    # 운동 사다리
    ladder_level: Mapped[int] = mapped_column(Integer, default=0)
    ladder_last_change: Mapped[date] = mapped_column(Date)
    ladder_restart_pending: Mapped[bool] = mapped_column(Boolean, default=False)
    ladder_checked_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    ladder_last_code: Mapped[str | None] = mapped_column(String(32), nullable=True)


class Consent(Base):
    """동의 이력. 종류별 가장 최근 행이 현재 상태. 철회도 행으로 남긴다."""
    __tablename__ = "consents"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(32))     # health | guardian_cheer_request | manager | location
    granted: Mapped[bool] = mapped_column(Boolean)
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))   # 본인 또는 대리 설정한 사람
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class GuardianLink(Base):
    __tablename__ = "guardian_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    guardian_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(16))   # pending | active | revoked
    # 어르신이 고르는 공유 범위. 기본은 응급만.
    scope: Mapped[str] = mapped_column(String(16), default="emergency_only")  # emergency_only | cheer_only | full
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("elder_id", "guardian_id"),)


class Precheck(Base):
    __tablename__ = "prechecks"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    inputs: Mapped[dict] = mapped_column(JSON)
    outcome: Mapped[str] = mapped_column(String(16))
    reasons: Mapped[list] = mapped_column(JSON)
    rule_version: Mapped[str] = mapped_column(String(32))
    plan: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    precheck_id: Mapped[int] = mapped_column(ForeignKey("prechecks.id"))
    day: Mapped[date] = mapped_column(Date, index=True)
    activity_id: Mapped[str] = mapped_column(String(32))
    kind: Mapped[str] = mapped_column(String(16))
    level: Mapped[int] = mapped_column(Integer)
    planned_minutes: Mapped[int] = mapped_column(Integer)
    hr_limits: Mapped[dict] = mapped_column(JSON)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    minutes: Mapped[float] = mapped_column(Float, default=0)
    max_rpe: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stopped: Mapped[bool] = mapped_column(Boolean, default=False)
    slow_recovery: Mapped[bool] = mapped_column(Boolean, default=False)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    intent: Mapped[str] = mapped_column(String(32))
    message_id: Mapped[str] = mapped_column(String(16))
    text: Mapped[str] = mapped_column(Text)
    cancel_if_done: Mapped[bool] = mapped_column(Boolean, default=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled: Mapped[bool] = mapped_column(Boolean, default=False)


class MessageUseRow(Base):
    __tablename__ = "message_uses"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    day: Mapped[date] = mapped_column(Date)
    message_id: Mapped[str] = mapped_column(String(16))


class GuardianAlert(Base):
    __tablename__ = "guardian_alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    guardian_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)  # None: 담당자·관리자
    kind: Mapped[str] = mapped_column(String(32))
    payload: Mapped[dict] = mapped_column(JSON)       # 위치는 넣지 않는다
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Cheer(Base):
    __tablename__ = "cheers"
    id: Mapped[int] = mapped_column(primary_key=True)
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    guardian_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str | None] = mapped_column(String(200), nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    played_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AccessLog(Base):
    """보호자 열람 로그(8장)."""
    __tablename__ = "access_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    viewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    what: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class JobRun(Base):
    __tablename__ = "job_runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job: Mapped[str] = mapped_column(String(32))
    elder_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    day: Mapped[date] = mapped_column(Date)
    result: Mapped[dict] = mapped_column(JSON)
    __table_args__ = (UniqueConstraint("job", "elder_id", "day"),)


class DecisionLogRow(Base):
    """변경 불가 판정 로그. 해시는 safety_engine.audit_log.record_hash와 같은 방식."""
    __tablename__ = "decision_log"
    seq: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    ts: Mapped[str] = mapped_column(String(40))
    user_id: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    rule_version: Mapped[str] = mapped_column(String(32))
    rule_sha256: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON)
    prev_hash: Mapped[str] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(64))


class LogChainHead(Base):
    """체인 끝을 한 행에 두고 SELECT ... FOR UPDATE로 잠가 동시 기록에도 순서가 꼬이지 않게 한다."""
    __tablename__ = "decision_log_head"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    next_seq: Mapped[int] = mapped_column(Integer)
    last_hash: Mapped[str] = mapped_column(String(64))


class ImmutableRowError(RuntimeError):
    pass


@event.listens_for(DecisionLogRow, "before_update")
@event.listens_for(DecisionLogRow, "before_delete")
def _forbid_change(mapper, connection, target):
    # 운영 DB에서는 이 테이블에 UPDATE/DELETE 권한 자체를 주지 않는다(README 참고).
    raise ImmutableRowError("decision_log is append-only")
