"""두 엔진과 DB를 잇는 어댑터: 판정 로그 저장, DB 행 → 엔진 입력 변환."""
import json
from datetime import date, datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from induction_engine import (History, LadderState, MessageUse, NotificationRecord, PrecheckRecord, SessionRecord,
                              UserProfile, load_config)
from safety_engine import DoctorLimits, Profile, SafetyEngine, load_rules
from safety_engine.audit_log import GENESIS, canonical, record_hash

from . import models as m
from .config import KST

HISTORY_DAYS = 60   # 상태·사다리·문구 반복 판단에 필요한 기간


class Engines:
    """프로세스당 한 번 로드. 규칙 번들은 버전·해시와 함께 판정 로그에 남는다."""

    def __init__(self, safety_rules=None, induction_cfg=None):
        self.safety_rules = safety_rules or load_rules()
        self.induction = induction_cfg or load_config()

    def safety(self, db, user_id):
        return SafetyEngine(self.safety_rules, DbDecisionLog(db, user_id))


class DbDecisionLog:
    """safety_engine.audit_log.DecisionLog와 같은 레코드·해시를 DB에 추가 전용으로 쓴다."""

    def __init__(self, db: Session, user_id=None):
        self.db = db
        self.user_id = user_id

    def append(self, kind, payload, rule_version, rule_sha256, ts=None):
        head = self.db.execute(select(m.LogChainHead).where(m.LogChainHead.id == 1).with_for_update()).scalar_one_or_none()
        if head is None:
            head = m.LogChainHead(id=1, next_seq=0, last_hash=GENESIS)
            self.db.add(head)
        rec = {
            "seq": head.next_seq,
            "ts": ts or datetime.now().astimezone().isoformat(),
            "user_id": self.user_id,
            "kind": kind,
            "rule_version": rule_version,
            "rule_sha256": rule_sha256,
            "payload": json.loads(canonical(payload)),   # 저장·재계산 표현을 맞춘다(날짜 → 문자열)
            "prev_hash": head.last_hash,
        }
        rec["hash"] = record_hash(rec)
        self.db.add(m.DecisionLogRow(**rec))
        head.next_seq += 1
        head.last_hash = rec["hash"]
        self.db.flush()
        return rec


def verify_log(db: Session):
    prev, expected = GENESIS, 0
    for row in db.execute(select(m.DecisionLogRow).order_by(m.DecisionLogRow.seq)).scalars():
        rec = {c: getattr(row, c) for c in ("seq", "ts", "user_id", "kind", "rule_version", "rule_sha256",
                                            "payload", "prev_hash", "hash")}
        if row.seq != expected or row.prev_hash != prev or row.hash != record_hash(rec):
            return False, expected
        prev, expected = row.hash, expected + 1
    return True, None


# ---- DB → 안전 엔진 ----
def safety_profile(profile: m.ElderProfile, today: date) -> Profile:
    h = profile.health or {}
    limits = h.get("doctor_limits") or {}
    return Profile(
        age=today.year - profile.birth_year,
        conditions=frozenset(h.get("conditions", [])),
        parq_risk=h.get("parq_risk", False),
        doctor_clearance=h.get("doctor_clearance", False),
        device=h.get("device"),
        beta_blocker=h.get("beta_blocker", False),
        doctor_limits=DoctorLimits(**limits),
    )


# ---- DB → 유도 엔진 ----
def latest_consents(db: Session, elder_id):
    rows = db.execute(select(m.Consent).where(m.Consent.elder_id == elder_id).order_by(m.Consent.id)).scalars()
    current = {}
    for c in rows:
        current[c.kind] = c.granted
    return current


def active_links(db: Session, elder_id):
    return list(db.execute(select(m.GuardianLink).where(
        m.GuardianLink.elder_id == elder_id, m.GuardianLink.status == "active")).scalars())


def induction_profile(db: Session, profile: m.ElderProfile) -> UserProfile:
    consents = latest_consents(db, profile.user_id)
    scopes = {link.scope for link in active_links(db, profile.user_id)}
    mode = "full" if "full" in scopes else "cheer_only" if "cheer_only" in scopes else "none"
    has_cheer = db.execute(select(m.Cheer.id).where(m.Cheer.elder_id == profile.user_id).limit(1)).first() is not None
    h, mi = map(int, profile.preferred_time.split(":"))
    return UserProfile(
        signup_date=profile.signup_date, preferred_time=time(h, mi), anchor=profile.anchor, goal=profile.goal,
        fall_concern=profile.fall_concern, guardian_mode=mode,
        consent_guardian_cheer_request=consents.get("guardian_cheer_request", False),
        has_guardian_cheer=has_cheer, manager_linked=False, consent_manager=consents.get("manager", False),
    )


def ladder_state(profile: m.ElderProfile) -> LadderState:
    return LadderState(profile.ladder_level, profile.ladder_last_change, profile.ladder_restart_pending)


def build_history(db: Session, elder_id, today: date) -> History:
    since = today - timedelta(days=HISTORY_DAYS)
    sessions = db.execute(select(m.ExerciseSession).where(
        m.ExerciseSession.elder_id == elder_id, m.ExerciseSession.day >= since)).scalars()
    prechecks = db.execute(select(m.Precheck).where(m.Precheck.elder_id == elder_id, m.Precheck.day >= since)).scalars()
    notes = db.execute(select(m.Notification).where(
        m.Notification.elder_id == elder_id, m.Notification.day >= since, m.Notification.sent_at.is_not(None))).scalars()
    uses = db.execute(select(m.MessageUseRow).where(
        m.MessageUseRow.elder_id == elder_id, m.MessageUseRow.day >= since)).scalars()
    return History(
        sessions=tuple(SessionRecord(
            day=s.day, completed=s.completed, minutes=s.minutes, level=s.level, kind=s.kind,
            activity_id=s.activity_id, stopped=s.stopped, max_rpe=s.max_rpe,
            start_time=_as_aware(s.started_at).astimezone(KST).time().replace(second=0, microsecond=0),
            slow_recovery=s.slow_recovery) for s in sessions),
        prechecks=tuple(PrecheckRecord(p.day, p.outcome) for p in prechecks),
        notifications=tuple(NotificationRecord(
            _as_aware(n.sent_at), n.message_id,
            n.opened_at is not None and _as_aware(n.opened_at) - _as_aware(n.sent_at) <= timedelta(minutes=60))
            for n in notes),
        messages=tuple(MessageUse(u.day, u.message_id) for u in uses),
    )


def _as_aware(dt):
    # SQLite는 시간대를 버리므로 저장값을 한국 시간으로 간주한다(운영 PostgreSQL은 timestamptz).
    return dt if dt.tzinfo else dt.replace(tzinfo=KST)


def record_message_use(db: Session, elder_id, day, message):
    if message is not None:
        db.add(m.MessageUseRow(elder_id=elder_id, day=day, message_id=message.id))
