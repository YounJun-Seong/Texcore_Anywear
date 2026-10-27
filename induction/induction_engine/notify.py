"""알림 시각·개수·피로 관리(6-3: R11~R13)."""
import statistics
from datetime import datetime, time, timedelta

from .history import completed
from .ladder import step_minutes
from .messages import pick_message


def _t(s):
    h, m = map(int, s.split(":"))
    return h * 60 + m


def _clock(minutes):
    return time(minutes // 60, minutes % 60)


def _minutes(t):
    return t.hour * 60 + t.minute


def pick_time(cfg, profile, history, today):
    """R11: 최근 실제 시작 시각 중앙값(3회 이상), 없으면 온보딩에서 고른 시간. 07:00~20:00 안으로."""
    n = cfg["notifications"]
    starts = [s.start_time for s in sorted(completed(history.sessions, end=today), key=lambda s: s.day, reverse=True)
              if s.start_time is not None][: n["median_window_sessions"]]
    if len(starts) >= n["median_min_samples"]:
        base, code = statistics.median_low(_minutes(t) for t in starts), "TIME_LEARNED"
    else:
        base, code = _minutes(profile.preferred_time), "TIME_PREFERRED"
    r = n["round_minutes"]
    rounded = (base + r // 2) // r * r
    lo, hi = _t(n["window"]["start"]), _t(n["window"]["end"]) - r
    clamped = min(max(rounded, lo), hi)
    if clamped != rounded:
        code = "TIME_CLAMPED"
    return _clock(clamped), code


def is_fatigued(cfg, history):
    """R13: 가장 최근 알림 N개를 연속으로 무시했는가."""
    k = cfg["notifications"]["consecutive_ignored_to_reduce"]
    recent = sorted(history.notifications, key=lambda n: n.sent_at)[-k:]
    return len(recent) == k and not any(n.opened for n in recent)


def plan_notifications(cfg, profile, history, today, level):
    """
    오늘 보낼 알림(R12: 최대 2개, 07:00~20:00). 운동을 마치면 앱이 남은 알림을 취소한다(cancel_if_done).
    """
    n = cfg["notifications"]
    fatigued = is_fatigued(cfg, history)
    limit = n["reduced_max_per_day"] if fatigued else n["max_per_day"]
    main_time, time_code = pick_time(cfg, profile, history, today)
    values = {"minutes": step_minutes(cfg, level)}

    picked = []
    intent = "reminder_bp" if profile.anchor == "bp" else "reminder"
    msg, _ = pick_message(cfg, intent, history.messages, today, values)
    picked.append({"time": main_time, "intent": intent, "message": msg, "cancel_if_done": True})

    ev = n["evening_nudge"]
    ev_time = _t(ev["time"])
    if (len(picked) < limit and _minutes(main_time) + ev["min_gap_minutes"] <= ev_time
            and _t(n["window"]["start"]) <= ev_time < _t(n["window"]["end"])):
        msg, _ = pick_message(cfg, "evening_mini", history.messages, today, values,
                              exclude=[p["message"].id for p in picked])
        picked.append({"time": _clock(ev_time), "intent": "evening_mini", "message": msg, "cancel_if_done": True})

    rules = ["R11", "R12"] + (["R13"] if fatigued else [])
    return {"items": picked[:limit], "fatigued": fatigued, "ask_time_change": fatigued,
            "time_code": time_code, "rules_fired": rules,
            "scheduled_for": [datetime.combine(today, p["time"]) for p in picked[:limit]]}
