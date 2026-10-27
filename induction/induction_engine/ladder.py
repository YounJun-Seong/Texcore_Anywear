"""'아주 작은 시작' 운동 사다리(6-2)와 주간·하루 상한."""
import math
from dataclasses import replace
from datetime import timedelta

from .history import BAD_LIGHTS, completed, last_completed_day, minutes_in, missed_days, week_window
from .types import LadderState


def step_minutes(cfg, level):
    return cfg["ladder"]["steps_minutes"][level]


def ladder_update(cfg, ladder: LadderState, history, signup_date, today):
    """
    하루 한 번(첫 화면 진입 시) 호출. 반환: (새 LadderState, 사유 코드)
    강등이 승급보다 먼저다. 강등 = 실패가 아니라 다음 운동을 더 안전하게.
    """
    lad = cfg["ladder"]
    since = ladder.last_change

    # R10: 마지막 변경 이후 중단·빨강·RPE 14 이상 → 한 단계 내림
    bad_session = any(s.day > since and s.day <= today and
                      (s.stopped or (s.max_rpe is not None and s.max_rpe >= lad["demote"]["rpe_at"]))
                      for s in history.sessions)
    bad_light = any(p.day > since and p.day <= today and p.light in BAD_LIGHTS for p in history.prechecks)
    if bad_session or bad_light:
        return _change(ladder, ladder.level - 1, today), "LADDER_DOWN_SAFETY"

    missed = missed_days(history.sessions, signup_date, today)
    # R15: 14일 → 새로 시작(사다리 처음, 사용자가 다시 하기/쉬기 선택)
    if missed >= lad["restart_missed_days"]:
        if ladder.restart_pending:
            return ladder, "LADDER_RESTART_PENDING"
        return LadderState(level=0, last_change=today, restart_pending=True), "LADDER_RESTART"

    # R10: 2일 연속 미실행 → 한 단계 내림(공백 하나에 한 번만)
    last_done = last_completed_day(history.sessions, today) or (signup_date - timedelta(days=1))
    trigger_day = last_done + timedelta(days=lad["demote"]["missed_days"] + 1)
    if missed >= lad["demote"]["missed_days"] and ladder.last_change < trigger_day and ladder.level > 0:
        return _change(ladder, ladder.level - 1, today), "LADDER_DOWN_MISSED"

    # R09: 현재 단계에 7일 이상 머물렀고, 최근 7일 이 단계로 4회 이상 완료 → 한 단계 올림
    start, end = week_window(today)
    at_level = [s for s in completed(history.sessions, start, end) if s.level == ladder.level]
    if ((today - since).days >= lad["promote"]["min_days_at_level"]
            and len(at_level) >= lad["promote"]["min_completed_at_level_7d"]
            and ladder.level < len(lad["steps_minutes"]) - 1):
        return _change(ladder, ladder.level + 1, today), "LADDER_UP"
    return ladder, "LADDER_HOLD"


def _change(ladder, level, today):
    return replace(ladder, level=max(0, level), last_change=today, restart_pending=False)


def minutes_budget(cfg, level, history, today):
    """
    오늘 더 할 수 있는 분.
    R07 하루 상한 60분, R08 주간 총량은 직전 7일의 110%까지
    (단, 운동량이 아주 적을 때는 '현재 단계 × 4회'까지 허용).
    """
    lad = cfg["ladder"]
    today_done = minutes_in(history.sessions, today, today)
    this_start, _ = week_window(today)
    last_start, last_end = week_window(today, 1)
    this_week = minutes_in(history.sessions, this_start, today)
    last_week = minutes_in(history.sessions, last_start, last_end)
    weekly_cap = max(last_week * (1 + lad["weekly_increase_max"]), step_minutes(cfg, level) * lad["weekly_floor_sessions"])
    daily_left = lad["daily_cap_minutes"] - today_done
    weekly_left = weekly_cap - this_week
    return {
        "daily_left": daily_left,
        "weekly_left": weekly_left,
        "minutes": max(0, math.floor(round(min(daily_left, weekly_left), 6))),
        "binding": "daily" if daily_left <= weekly_left else "weekly",
    }
