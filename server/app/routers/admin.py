"""관리자 콘솔(최소): 사용자, 안전 이벤트(판정 로그), 로그 무결성, 스케줄러 수동 실행, 담당자 연계 대기."""
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models as m
from ..deps import AppContext, admin_user, ctx, get_db
from ..engines import verify_log
from ..services import dispatch_due, run_daily

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(admin_user)])


@router.get("/users")
def users(db: Session = Depends(get_db)):
    return [{"id": u.id, "role": u.role, "name": u.name, "active": u.active}
            for u in db.execute(select(m.User).order_by(m.User.id)).scalars()]


@router.get("/decision-log")
def decision_log(user_id: int | None = None, kind: str | None = None, limit: int = 100,
                 db: Session = Depends(get_db)):
    q = select(m.DecisionLogRow).order_by(m.DecisionLogRow.seq.desc()).limit(min(limit, 1000))
    if user_id is not None:
        q = q.where(m.DecisionLogRow.user_id == user_id)
    if kind:
        q = q.where(m.DecisionLogRow.kind == kind)
    return [{"seq": r.seq, "ts": r.ts, "user_id": r.user_id, "kind": r.kind, "rule_version": r.rule_version,
             "payload": r.payload} for r in db.execute(q).scalars()]


@router.get("/decision-log/verify")
def verify(db: Session = Depends(get_db)):
    ok, broken_at = verify_log(db)
    return {"ok": ok, "broken_at": broken_at}


@router.get("/alerts")
def staff_alerts(db: Session = Depends(get_db)):
    """보호자에게 가지 않는 알림(보건소·복지관 담당자 전화 권유 등)."""
    rows = db.execute(select(m.GuardianAlert).where(m.GuardianAlert.guardian_id.is_(None))
                      .order_by(m.GuardianAlert.id.desc())).scalars()
    return [{"id": a.id, "elder_id": a.elder_id, "kind": a.kind, "payload": a.payload, "at": a.created_at}
            for a in rows]


@router.post("/jobs/daily")
def job_daily(day: date | None = None, db: Session = Depends(get_db), c: AppContext = Depends(ctx)):
    return {"day": day or c.clock.today(), "elders": run_daily(db, c, day or c.clock.today())}


@router.post("/jobs/dispatch")
def job_dispatch(db: Session = Depends(get_db), c: AppContext = Depends(ctx)):
    return dispatch_due(db, c, c.clock.now())
