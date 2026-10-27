"""보호자 알림 라우팅과 하루 스케줄러(사다리·알림·재참여)."""
from dataclasses import asdict
from datetime import datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from induction_engine import (classify_state, day_reward, ladder_message, ladder_update, plan_notifications,
                              reengagement, streak, weekly_stamps)
from induction_engine.history import completed, minutes_in, week_window

from . import models as m
from .config import KST
from .deps import AppContext
from .engines import (_as_aware, active_links, build_history, induction_profile, ladder_state, latest_consents,
                      record_message_use)
from .gateway import Outbound

ALL_SCOPES = {"emergency_only", "cheer_only", "full"}
FULL = {"full"}
ELDER_PROMPTS = {"ask_reason", "cause_check", "restart_offer", "play_guardian_cheer"}


# ---- 보호자 알림 ----
def alert_guardians(db: Session, c: AppContext, elder: m.User, kind, payload, scopes, body,
                    location=None, call=False):
    """
    scopes: 이 알림을 받을 공유 범위. 응급은 모든 범위, 운동 여부·요약은 full만.
    location: 응급 시에만, 위치 동의가 있을 때만 전송. DB에는 저장하지 않는다.
    """
    sent = 0
    for link in active_links(db, elder.id):
        if link.scope not in scopes:
            continue
        guardian = db.get(m.User, link.guardian_id)
        db.add(m.GuardianAlert(elder_id=elder.id, guardian_id=guardian.id, kind=kind, payload=payload,
                               created_at=c.clock.now()))
        data = {"kind": kind, "elder_id": elder.id, **payload}
        if location is not None:
            data["location"] = location
        if call:
            c.gateway.send(Outbound("call", guardian.id, guardian.phone, f"{elder.name}님 확인 필요", body, data))
        c.gateway.send(Outbound("push", guardian.id, guardian.phone, f"{elder.name}님", body, data))
        sent += 1
    return sent


def week_summary(history, today):
    start, _ = week_window(today)
    return {"stamps": weekly_stamps(history, today), "sessions": len(completed(history.sessions, start, today)),
            "minutes": round(minutes_in(history.sessions, start, today))}


# ---- 하루 처리 ----
def ensure_ladder(db: Session, c: AppContext, profile: m.ElderProfile, today):
    """하루 한 번 사다리 갱신. 같은 날 다시 불러도 바뀌지 않는다."""
    if profile.ladder_checked_on == today:
        return profile.ladder_last_code, None
    history = build_history(db, profile.user_id, today)
    new, code = ladder_update(c.engines.induction, ladder_state(profile), history, profile.signup_date, today)
    profile.ladder_level, profile.ladder_last_change = new.level, new.last_change
    profile.ladder_restart_pending = new.restart_pending
    profile.ladder_checked_on, profile.ladder_last_code = today, code
    msg = ladder_message(c.engines.induction, history, today, new, code)
    record_message_use(db, profile.user_id, today, msg)
    return code, msg


def run_daily_for(db: Session, c: AppContext, elder: m.User, today):
    """사다리 → 오늘 알림 예약 → 재참여. (job, 사람, 날짜)마다 한 번만 실행되고 결과를 남긴다."""
    done = db.execute(select(m.JobRun).where(m.JobRun.job == "daily", m.JobRun.elder_id == elder.id,
                                             m.JobRun.day == today)).scalar_one_or_none()
    if done is not None:
        return done.result
    cfg = c.engines.induction
    profile = db.get(m.ElderProfile, elder.id)
    ladder_code, ladder_msg = ensure_ladder(db, c, profile, today)
    db.flush()

    history = build_history(db, elder.id, today)
    uprofile = induction_profile(db, profile)
    plan = plan_notifications(cfg, uprofile, history, today, profile.ladder_level)
    for item in plan["items"]:
        db.add(m.Notification(elder_id=elder.id, day=today, intent=item["intent"], message_id=item["message"].id,
                              text=item["message"].text, cancel_if_done=item["cancel_if_done"],
                              scheduled_at=datetime.combine(today, item["time"], tzinfo=KST)))
        record_message_use(db, elder.id, today, item["message"])

    reeng = reengagement(cfg, uprofile, history, today)
    guardian_actions = []
    for action in reeng["actions"]:
        if action == "request_guardian_cheer":
            alert_guardians(db, c, elder, "cheer_request", {}, FULL, "응원 한마디 보내 주세요")
        elif action == "guardian_weekly_summary":
            alert_guardians(db, c, elder, "weekly_summary", week_summary(history, today), FULL, "이번 주 요약이 왔어요")
        elif action == "guardian_lapse_alert":
            alert_guardians(db, c, elder, "lapse", {"missed_days": reeng["missed_days"]}, FULL,
                            "요즘 운동을 쉬고 계세요. 안부 전화 한 통 어떠세요?")
        elif action == "manager_call":
            db.add(m.GuardianAlert(elder_id=elder.id, guardian_id=None, kind="manager_call",
                                   payload={"missed_days": reeng["missed_days"]}, created_at=c.clock.now()))
        else:
            continue
        guardian_actions.append(action)

    result = {
        "ladder": {"code": ladder_code, "level": profile.ladder_level,
                   "message": ladder_msg.text if ladder_msg else None,
                   "restart_pending": profile.ladder_restart_pending},
        "notifications": {"count": len(plan["items"]), "fatigued": plan["fatigued"],
                          "ask_time_change": plan["ask_time_change"], "rules_fired": plan["rules_fired"]},
        "reengagement": {"tier": reeng["tier"], "missed_days": reeng["missed_days"],
                         "prompts": [a for a in reeng["actions"] if a in ELDER_PROMPTS],
                         "guardian_actions": guardian_actions, "withheld": reeng["withheld"]},
    }
    db.add(m.JobRun(job="daily", elder_id=elder.id, day=today, result=result))
    db.flush()
    return result


def run_daily(db: Session, c: AppContext, today):
    elders = db.execute(select(m.User).where(m.User.role == "elder", m.User.active.is_(True))).scalars().all()
    return {e.id: run_daily_for(db, c, e, today) for e in elders}


def dispatch_due(db: Session, c: AppContext, now: datetime):
    """예약 시각이 지난 알림 발송. 오늘 운동을 마쳤으면 취소, 07:00~20:00 밖이면 보내지 않는다."""
    window = c.engines.induction["notifications"]["window"]
    start, end = (time(*map(int, window[k].split(":"))) for k in ("start", "end"))
    due = db.execute(select(m.Notification).where(m.Notification.sent_at.is_(None),
                                                  m.Notification.cancelled.is_(False))).scalars().all()
    sent = cancelled = 0
    for n in due:
        at = _as_aware(n.scheduled_at)
        if at > now:
            continue
        local = now.astimezone(KST)
        done_today = db.execute(select(m.ExerciseSession.id).where(
            m.ExerciseSession.elder_id == n.elder_id, m.ExerciseSession.day == n.day,
            m.ExerciseSession.completed.is_(True))).first() is not None
        if (n.cancel_if_done and done_today) or local.date() != n.day or not (start <= local.time() < end):
            n.cancelled = True
            cancelled += 1
            continue
        elder = db.get(m.User, n.elder_id)
        c.gateway.send(Outbound("push", elder.id, elder.phone, "운동 알림", n.text,
                                {"notification_id": n.id, "intent": n.intent}))
        n.sent_at = now
        sent += 1
    return {"sent": sent, "cancelled": cancelled}


def today_rewards(db: Session, elder_id, today):
    history = build_history(db, elder_id, today)
    return {"today": day_reward(history, today), "streak": streak(history, today),
            "weekly_stamps": weekly_stamps(history, today)}


def has_consent(db: Session, elder_id, kind):
    return latest_consents(db, elder_id).get(kind, False)


def user_state(c: AppContext, db: Session, profile: m.ElderProfile, today):
    history = build_history(db, profile.user_id, today)
    return classify_state(c.engines.induction, history.sessions, profile.signup_date, today).value


def plan_to_dict(plan):
    d = asdict(plan)
    d["rules_fired"] = list(plan.rules_fired)
    return d


def days_back(today, n):
    return [today - timedelta(days=i) for i in range(n - 1, -1, -1)]
