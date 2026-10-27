from datetime import datetime, time, timedelta

import pytest

from induction_engine import MessageUse, NotificationRecord, UserProfile, UserState, Weather, pick_time, plan_notifications
from induction_engine.activity import pick_activity, pick_kind, weather_reason
from induction_engine.messages import pick_message

from conftest import D0, day, hist, sess


# ---- 날씨 (R06) ----
@pytest.mark.parametrize("w,expected", [
    (None, None), (Weather(), None), (Weather(temp_c=15, pm10=30, pm25=15), None),
    (Weather(precipitation=True), "precipitation"),
    (Weather(temp_c=-0.5), "cold"), (Weather(temp_c=0), None),
    (Weather(temp_c=33), "heat"), (Weather(temp_c=32.9), None),
    (Weather(pm10=81), "dust"), (Weather(pm10=80), None), (Weather(pm25=36), "dust"), (Weather(pm25=35), None),
])
def test_weather_reason(cfg, w, expected):
    assert weather_reason(cfg, w) == expected


@pytest.mark.parametrize("key", ["precipitation", "cold", "heat", "dust"])
def test_bad_weather_never_outdoor(cfg, key):
    for n in range(10):
        a = pick_activity(cfg, hist([sess(i, kind="strength") for i in range(n)]), day(10), "moderate",
                          UserState.HABIT, key, False)
        assert a["indoor"]


# ---- 종류 비율 (R05) ----
def test_weekly_mix_follows_2_1_1(cfg):
    sessions, kinds = [], []
    for i in range(8):
        k = pick_kind(cfg, hist(sessions), day(i), False, {"aerobic", "strength", "balance"})
        kinds.append(k)
        sessions.append(sess(i, kind=k))
    week = kinds[1:8]   # 마지막 7일
    assert kinds[:4] == ["aerobic", "strength", "balance", "aerobic"]
    assert week.count("aerobic") >= 3 and week.count("strength") >= 1 and week.count("balance") >= 1


def test_fall_concern_more_balance_and_always_supported(cfg):
    sessions, kinds = [], []
    for i in range(10):
        a = pick_activity(cfg, hist(sessions), day(i), "moderate", UserState.HABIT, None, True)
        assert a["supported"]
        kinds.append(a["kind"])
        sessions.append(sess(i, kind=a["kind"], activity_id=a["id"]))
    assert kinds[-7:].count("balance") >= 2


def test_fear_state_seated_only_and_yellow_low_only(cfg):
    for n in range(6):
        h = hist([sess(i, kind=k) for i, k in zip(range(n), ["aerobic", "strength", "balance"] * 2)])
        assert pick_activity(cfg, h, day(10), "moderate", UserState.FEAR, None, False)["seated"]
        assert pick_activity(cfg, h, day(10), "low", UserState.HABIT, None, False)["intensity"] == "low"


def test_variety_prefers_least_recent(cfg):
    # 이번 주(2~8일): 걷기 2, 힘 1 → 균형 차례. 지난주에 한 supported_balance 대신 free_balance
    h = hist([sess(0, kind="balance", activity_id="supported_balance"),
              sess(3), sess(4), sess(5, kind="strength")])
    picked = pick_activity(cfg, h, day(8), "moderate", UserState.HABIT, None, False)
    assert picked["id"] == "free_balance"


# ---- 알림 시각 (R11) ----
def test_time_uses_preferred_until_3_samples(cfg):
    p = UserProfile(signup_date=D0, preferred_time=time(10, 0))
    h = hist([sess(1, start_time=time(8, 0)), sess(2, start_time=time(8, 10))])
    assert pick_time(cfg, p, h, day(3)) == (time(10, 0), "TIME_PREFERRED")


def test_time_learns_median_rounded_to_5(cfg):
    p = UserProfile(signup_date=D0, preferred_time=time(10, 0))
    starts = [time(8, 2), time(8, 13), time(17, 0), time(8, 21)]
    h = hist([sess(i + 1, start_time=t) for i, t in enumerate(starts)])
    assert pick_time(cfg, p, h, day(5)) == (time(8, 15), "TIME_LEARNED")   # 하위 중앙값 08:13 → 08:15


@pytest.mark.parametrize("pref,expected", [(time(5, 30), time(7, 0)), (time(21, 30), time(19, 55)),
                                           (time(19, 58), time(19, 55)), (time(7, 0), time(7, 0))])
def test_time_clamped_to_window(cfg, pref, expected):
    t, code = pick_time(cfg, UserProfile(signup_date=D0, preferred_time=pref), hist(), day(1))
    assert t == expected


@pytest.mark.parametrize("hour", range(0, 24))
def test_notifications_never_outside_window_or_over_two(cfg, hour):
    plan = plan_notifications(cfg, UserProfile(signup_date=D0, preferred_time=time(hour, 30)), hist(), day(1), 0)
    assert 1 <= len(plan["items"]) <= 2
    for item in plan["items"]:
        assert time(7, 0) <= item["time"] < time(20, 0)
    ids = [i["message"].id for i in plan["items"]]
    assert len(ids) == len(set(ids))


def test_evening_nudge_only_with_enough_gap(cfg):
    early = plan_notifications(cfg, UserProfile(signup_date=D0, preferred_time=time(9, 0)), hist(), day(1), 0)
    late = plan_notifications(cfg, UserProfile(signup_date=D0, preferred_time=time(18, 30)), hist(), day(1), 0)
    assert [i["intent"] for i in early["items"]] == ["reminder", "evening_mini"]
    assert [i["intent"] for i in late["items"]] == ["reminder"]


def test_bp_anchor_reminder(cfg):
    plan = plan_notifications(cfg, UserProfile(signup_date=D0, anchor="bp"), hist(), day(1), 0)
    assert plan["items"][0]["intent"] == "reminder_bp"


# ---- 알림 피로 (R13) ----
def _notes(*opened):
    return [NotificationRecord(datetime(2026, 10, 1, 9) + timedelta(days=i), "a01", o) for i, o in enumerate(opened)]


@pytest.mark.parametrize("opened,fatigued", [
    ((), False), ((False,), False), ((True, False), False), ((False, False), True),
    ((True, False, False), True), ((False, False, True), False),
])
def test_fatigue_after_two_ignored(cfg, opened, fatigued):
    plan = plan_notifications(cfg, UserProfile(signup_date=D0), hist(notifications=_notes(*opened)), day(10), 0)
    assert plan["fatigued"] == fatigued and plan["ask_time_change"] == fatigued
    assert len(plan["items"]) == (1 if fatigued else 2)


# ---- 문구 반복 금지 (R14) ----
def test_no_repeat_within_14_days(cfg):
    used = []
    seen = []
    for d in range(14):
        m, code = pick_message(cfg, "complete", used, day(d))
        assert code == "MSG_FRESH" or len([x for x in cfg.messages if x["intent"] == "complete"]) <= d
        seen.append((d, m.id))
        used.append(MessageUse(day(d), m.id))
    for (d1, a), (d2, b) in zip(seen, seen[1:]):
        assert a != b


def test_reuse_allowed_on_day_14_not_13(cfg):
    pool = [m["id"] for m in cfg.messages if m["intent"] == "rest_red"]
    used13 = [MessageUse(day(0), mid) for mid in pool[1:]] + [MessageUse(day(1), pool[0])]
    m, code = pick_message(cfg, "rest_red", used13, day(14))      # pool[0]은 13일 전 → 막힘, 나머지 14일 전 → 허용
    assert m.id == pool[1] and code == "MSG_FRESH"
    m, code = pick_message(cfg, "rest_red", [MessageUse(day(5), mid) for mid in pool], day(10))
    assert code == "MSG_REPEAT_FALLBACK"


def test_goal_templates_skipped_without_goal(cfg):
    m, _ = pick_message(cfg, "today_FEAR", [], day(1), {"minutes": 3, "activity": "x", "goal": None})
    assert "{" not in m.text
