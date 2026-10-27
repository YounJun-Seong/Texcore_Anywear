"""보호자: 연결, 대리 설정, 공유 범위에 맞춘 요약, 알림, 응원.

어르신이 고른 공유 범위만 본다.
  emergency_only: 응급 알림만 / cheer_only: 응원 보내기만(운동 여부 안 보임) / full: 오늘 했는지·주간 요약
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models as m
from ..deps import AppContext, ctx, get_db, guardian_user
from ..engines import build_history
from ..services import today_rewards, week_summary
from .auth import create_elder, normalize_phone
from .me import HealthIn, SettingsIn, record_consent, save_health, save_settings

router = APIRouter(prefix="/guardian", tags=["guardian"])


class LinkRequest(BaseModel):
    elder_phone: str


class ProxyElderIn(BaseModel):
    """보건소·복지관 직원이나 자녀가 대신 가입시키는 '대리 설정'. 대리 동의의 법적 범위는 법률 검토 대상(8장)."""
    phone: str
    name: str = Field(max_length=64)
    birth_year: int = Field(ge=1900, le=2010)
    consent_health: bool
    health: HealthIn | None = None
    settings: SettingsIn | None = None


class CheerIn(BaseModel):
    text: str | None = Field(None, max_length=200)
    audio_url: str | None = Field(None, max_length=500)


def _link(db, guardian_id, elder_id, scopes=None):
    link = db.execute(select(m.GuardianLink).where(
        m.GuardianLink.guardian_id == guardian_id, m.GuardianLink.elder_id == elder_id,
        m.GuardianLink.status == "active")).scalar_one_or_none()
    if link is None or (scopes and link.scope not in scopes):
        raise HTTPException(404 if link is None else 403, "볼 수 있는 정보가 없어요")
    return link


@router.post("/links")
def request_link(body: LinkRequest, user: m.User = Depends(guardian_user), db: Session = Depends(get_db),
                 c: AppContext = Depends(ctx)):
    elder = db.execute(select(m.User).where(m.User.phone == normalize_phone(body.elder_phone),
                                            m.User.role == "elder")).scalar_one_or_none()
    if elder is None:
        raise HTTPException(404, "가입한 어르신을 찾을 수 없어요")
    existing = db.execute(select(m.GuardianLink).where(m.GuardianLink.elder_id == elder.id,
                                                       m.GuardianLink.guardian_id == user.id)).scalar_one_or_none()
    if existing:
        return {"link_id": existing.id, "status": existing.status}
    link = m.GuardianLink(elder_id=elder.id, guardian_id=user.id, status="pending", scope="emergency_only",
                          created_by=user.id, created_at=c.clock.now())
    db.add(link)
    db.flush()
    return {"link_id": link.id, "status": "pending"}   # 어르신이 수락하고 공유 범위를 고른다


@router.post("/elders")
def proxy_setup(body: ProxyElderIn, user: m.User = Depends(guardian_user), db: Session = Depends(get_db),
                c: AppContext = Depends(ctx)):
    phone = normalize_phone(body.phone)
    if db.execute(select(m.User.id).where(m.User.phone == phone)).first():
        raise HTTPException(409, "이미 가입한 번호예요. 연결 요청을 보내 주세요")
    elder = create_elder(db, c, phone, body.name, body.birth_year, proxy=True)
    # 대리 설정은 응급 공유만으로 시작. 더 넓은 공유는 어르신이 직접 고른다.
    db.add(m.GuardianLink(elder_id=elder.id, guardian_id=user.id, status="active", scope="emergency_only",
                          created_by=user.id, created_at=c.clock.now()))
    record_consent(db, c, elder.id, user.id, "health", body.consent_health)
    db.flush()
    profile = db.get(m.ElderProfile, elder.id)
    if body.health:
        save_health(db, c, profile, body.health)
    if body.settings:
        save_settings(profile, body.settings)
    return {"elder_id": elder.id, "scope": "emergency_only"}


@router.put("/elders/{elder_id}/health")
def proxy_health(elder_id: int, body: HealthIn, user: m.User = Depends(guardian_user),
                 db: Session = Depends(get_db), c: AppContext = Depends(ctx)):
    _link(db, user.id, elder_id)
    profile = db.get(m.ElderProfile, elder_id)
    if not profile.proxy_setup:
        raise HTTPException(403, "대리 설정한 경우에만 대신 입력할 수 있어요")
    save_health(db, c, profile, body)
    return {"saved": True}


@router.get("/elders")
def my_elders(user: m.User = Depends(guardian_user), db: Session = Depends(get_db)):
    links = db.execute(select(m.GuardianLink).where(m.GuardianLink.guardian_id == user.id)).scalars()
    return [{"elder_id": link.elder_id, "name": db.get(m.User, link.elder_id).name, "status": link.status,
             "scope": link.scope} for link in links]


@router.get("/elders/{elder_id}/summary")
def summary(elder_id: int, user: m.User = Depends(guardian_user), db: Session = Depends(get_db),
            c: AppContext = Depends(ctx)):
    link = _link(db, user.id, elder_id)
    db.add(m.AccessLog(viewer_id=user.id, elder_id=elder_id, what=f"summary:{link.scope}", created_at=c.clock.now()))
    out = {"elder_id": elder_id, "name": db.get(m.User, elder_id).name, "scope": link.scope,
           "can_cheer": link.scope in ("cheer_only", "full")}
    if link.scope == "full":
        day = c.clock.today()
        history = build_history(db, elder_id, day)
        rewards = today_rewards(db, elder_id, day)
        out.update(done_today=any(s.day == day and s.completed for s in history.sessions),
                   streak=rewards["streak"], week=week_summary(history, day))
    return out


@router.get("/alerts")
def alerts(user: m.User = Depends(guardian_user), db: Session = Depends(get_db)):
    rows = db.execute(select(m.GuardianAlert).where(m.GuardianAlert.guardian_id == user.id)
                      .order_by(m.GuardianAlert.id.desc()).limit(100)).scalars()
    return [{"id": a.id, "elder_id": a.elder_id, "kind": a.kind, "payload": a.payload, "at": a.created_at,
             "acknowledged": a.acknowledged_at is not None} for a in rows]


@router.post("/alerts/{alert_id}/ack")
def ack(alert_id: int, user: m.User = Depends(guardian_user), db: Session = Depends(get_db),
        c: AppContext = Depends(ctx)):
    a = db.get(m.GuardianAlert, alert_id)
    if a is None or a.guardian_id != user.id:
        raise HTTPException(404, "알림을 찾을 수 없어요")
    a.acknowledged_at = a.acknowledged_at or c.clock.now()
    return {"acknowledged": True}


@router.post("/elders/{elder_id}/cheers")
def cheer(elder_id: int, body: CheerIn, user: m.User = Depends(guardian_user), db: Session = Depends(get_db),
          c: AppContext = Depends(ctx)):
    _link(db, user.id, elder_id, scopes={"cheer_only", "full"})
    if not body.text and not body.audio_url:
        raise HTTPException(422, "응원 글이나 음성이 필요해요")
    row = m.Cheer(elder_id=elder_id, guardian_id=user.id, text=body.text, audio_url=body.audio_url,
                  created_at=c.clock.now())
    db.add(row)
    db.flush()
    return {"cheer_id": row.id}
