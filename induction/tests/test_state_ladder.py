import pytest

from induction_engine import LadderState, PrecheckRecord, UserState, classify_state, ladder_update, minutes_budget

from conftest import D0, day, hist, sess


def weeks_of(n_weeks, per_week, start=0, level=0):
    """start일부터 n주 동안 매주 앞쪽 per_week일에 운동."""
    return [sess(start + 7 * w + i, level) for w in range(n_weeks) for i in range(per_week)]


# ---- 상태 4단계 ----
@pytest.mark.parametrize("sessions,today,expected", [
    ([], 0, UserState.FEAR),
    ([sess(1), sess(3)], 10, UserState.FEAR),                   # 2회 이하
    ([sess(1)], 40, UserState.FEAR),                            # 2주가 지나도 2회 이하면 두려움
    ([sess(1), sess(3), sess(5)], 6, UserState.STARTING),
    (weeks_of(2, 3), 13, UserState.STARTING),                   # 주 3회지만 2주뿐
    (weeks_of(3, 2), 20, UserState.STARTING),                   # 3주지만 주 2회
    ([sess(i) for i in (0, 2, 4, 7, 9, 11, 14, 16, 18)], 18, UserState.HABIT),
    ([sess(i) for i in (0, 2, 4, 7, 9, 11, 14, 16, 18)], 20, UserState.HABIT),   # 공백 2일
    ([sess(i) for i in (0, 2, 4, 7, 9, 11, 14, 16, 18)], 21, UserState.LAPSE_RISK),  # 공백 3일 + 습관 이력
    (weeks_of(3, 3), 20, UserState.LAPSE_RISK),                 # 마지막 16일, 공백 4일
    ([sess(i) for i in (0, 2, 4, 7, 9, 11, 14, 16, 18, 22)], 23, UserState.STARTING),  # 이탈 위험에서 복귀, 최근 주 2회
])
def test_classify(cfg, sessions, today, expected):
    assert classify_state(cfg, sessions, D0, day(today)) == expected


def test_lapse_needs_habit_history(cfg):
    sessions = weeks_of(3, 3)                                   # 마지막 운동 day 16
    assert classify_state(cfg, sessions, D0, day(18)) == UserState.HABIT       # 공백 2일
    assert classify_state(cfg, sessions, D0, day(19)) == UserState.LAPSE_RISK  # 공백 3일
    assert classify_state(cfg, weeks_of(2, 3), D0, day(30)) == UserState.STARTING  # 습관 이력 없음


# ---- 사다리 ----
def test_promote_after_7_days_and_4_sessions(cfg):
    h = hist([sess(i) for i in (1, 2, 4, 6)])
    assert ladder_update(cfg, LadderState(0, D0), h, D0, day(7)) == (LadderState(1, day(7)), "LADDER_UP")


@pytest.mark.parametrize("sessions,today,why", [
    ([sess(i) for i in (1, 2, 4, 6)], 6, "6일만 머묾"),
    ([sess(i) for i in (2, 4, 6)], 7, "3회"),
    ([sess(i, level=1) for i in (1, 2, 4, 6)], 7, "다른 단계 기록"),
    ([sess(i, completed=False) for i in (1, 2, 4, 6)], 7, "미완료"),
])
def test_no_promotion(cfg, sessions, today, why):
    new, code = ladder_update(cfg, LadderState(0, D0), hist(sessions), D0, day(today))
    assert new.level == 0, why


@pytest.mark.parametrize("bad", [
    {"sessions": [sess(5, level=2, stopped=True)]},
    {"sessions": [sess(5, level=2, max_rpe=14)]},
    {"prechecks": [PrecheckRecord(day(5), "RED")]},
    {"prechecks": [PrecheckRecord(day(5), "EMERGENCY")]},
])
def test_demote_on_safety_signal_beats_promotion(cfg, bad):
    good = [sess(i, level=2) for i in (1, 2, 3, 4, 6)]
    h = hist(good + bad.get("sessions", []), bad.get("prechecks", []))
    assert ladder_update(cfg, LadderState(2, D0), h, D0, day(7)) == (LadderState(1, day(7)), "LADDER_DOWN_SAFETY")


def test_rpe_13_and_yellow_do_not_demote(cfg):
    h = hist([sess(3, level=2, max_rpe=13)], [PrecheckRecord(day(3), "YELLOW")])
    assert ladder_update(cfg, LadderState(2, D0), h, D0, day(4))[1] == "LADDER_HOLD"


def test_safety_signal_before_last_change_is_not_counted_twice(cfg):
    h = hist([sess(3, level=2, stopped=True), sess(5, level=1)])
    once, _ = ladder_update(cfg, LadderState(2, D0), h, D0, day(4))
    assert once == LadderState(1, day(4))
    assert ladder_update(cfg, once, h, D0, day(6))[1] == "LADDER_HOLD"


def test_missed_two_days_demotes_once_per_gap(cfg):
    h = hist([sess(10, level=3)])
    lad = LadderState(3, day(5))
    assert ladder_update(cfg, lad, h, D0, day(12))[1] == "LADDER_HOLD"        # 하루 미실행
    lad2, code = ladder_update(cfg, lad, h, D0, day(13))                      # 11·12일 미실행
    assert (lad2, code) == (LadderState(2, day(13)), "LADDER_DOWN_MISSED")
    assert ladder_update(cfg, lad2, h, D0, day(15))[1] == "LADDER_HOLD"       # 같은 공백에 또 내리지 않음


def test_promotion_during_gap_still_demotes(cfg):
    h = hist([sess(i, level=1) for i in (5, 6, 7, 8)])
    lad = LadderState(2, day(9))                                              # 9일에 승급, 이후 미실행
    assert ladder_update(cfg, lad, h, D0, day(11))[1] == "LADDER_DOWN_MISSED"


def test_restart_after_14_days(cfg):
    h = hist([sess(1, level=4)])
    lad, code = ladder_update(cfg, LadderState(4, day(1)), h, D0, day(16))
    assert (lad, code) == (LadderState(0, day(16), restart_pending=True), "LADDER_RESTART")
    assert ladder_update(cfg, lad, h, D0, day(17))[1] == "LADDER_RESTART_PENDING"


def test_level_bounds(cfg):
    assert ladder_update(cfg, LadderState(0, D0), hist([sess(1, stopped=True)]), D0, day(2))[0].level == 0
    top = len(cfg["ladder"]["steps_minutes"]) - 1
    h = hist([sess(i, level=top) for i in (3, 4, 5, 6)])
    assert ladder_update(cfg, LadderState(top, D0), h, D0, day(7))[0].level == top


# ---- 하루·주간 상한 ----
def test_daily_cap(cfg):
    h = hist([sess(10, level=6, minutes=30), sess(10, level=6, minutes=25)])
    b = minutes_budget(cfg, 6, h, day(10))
    assert b["daily_left"] == 5


def test_weekly_increase_limited_to_10_percent(cfg):
    last_week = [sess(i, level=5) for i in (1, 2, 3, 4, 5)]                  # 20분 × 5 = 100분
    this_week = [sess(i, level=5) for i in (8, 9, 10, 11, 12)]               # 100분
    b = minutes_budget(cfg, 5, hist(last_week + this_week), day(14))
    assert b["weekly_left"] == pytest.approx(10) and b["minutes"] == 10 and b["binding"] == "weekly"


def test_weekly_floor_allows_early_ladder_growth(cfg):
    last_week = [sess(i) for i in (1, 2, 3, 4)]                              # 3분 × 4 = 12분 → 110%면 13.2분
    b = minutes_budget(cfg, 1, hist(last_week), day(14))                     # 5분 단계 × 4회 = 20분까지
    assert b["weekly_left"] == 20
