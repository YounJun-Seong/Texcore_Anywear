import itertools

import pytest

from induction_engine import (LadderState, PrecheckRecord, UserProfile, Weather, completion_message, day_reward,
                              ladder_message, plan_today, reengagement, streak, weekly_stamps)
from safety_engine import Profile, Vitals
from safety_engine.precheck import allowance, pre_check

from conftest import D0, day, hist, sess

VITALS = {"GREEN": Vitals(130, 80, 70), "YELLOW": Vitals(165, 80, 70), "RED": Vitals(185, 80, 70),
          "REMEASURE": Vitals(300, 80, 70)}
ME = UserProfile(signup_date=D0)


def decision(srules, light, profile=Profile(age=74), symptoms=()):
    return pre_check(srules, profile, VITALS.get(light, VITALS["GREEN"]), symptoms)


# ---- 안전 엔진 결과 전달 (R01·R02) ----
def test_safety_outcomes_pass_through(cfg, srules):
    lad = LadderState(3, D0)
    em = plan_today(cfg, srules, ME, lad, hist(), decision(srules, "GREEN", symptoms=["chest_pain"]), day(1))
    assert (em.action, em.notify_guardian, em.minutes) == ("EMERGENCY", True, 0)
    blocked = plan_today(cfg, srules, ME, lad, hist(),
                         decision(srules, "GREEN", Profile(age=74, parq_risk=True)), day(1))
    assert blocked.action == "DOCTOR_CHECK" and blocked.minutes == 0
    assert plan_today(cfg, srules, ME, lad, hist(), decision(srules, "REMEASURE"), day(1)).action == "REMEASURE"
    red = plan_today(cfg, srules, ME, lad, hist(), decision(srules, "RED"), day(1))
    assert red.action == "REST_AND_PRAISE" and red.minutes == 0 and red.detail["stamp"]
    assert red.message.intent == "rest_red"


# ---- 안전이 항상 이긴다: 모든 조합에서 허용 범위를 넘지 않음 ----
def _histories():
    yield hist()
    yield hist([sess(i) for i in range(5)])
    yield hist([sess(i, level=4) for i in range(0, 21, 2)])
    yield hist([sess(20, level=6, minutes=50)])                       # 오늘 이미 50분
    yield hist([sess(19, level=3, slow_recovery=True)])


@pytest.mark.parametrize("light,level,weather,fall", list(itertools.product(
    ["GREEN", "YELLOW"], range(7), [None, Weather(precipitation=True)], [False, True])))
def test_plan_never_exceeds_safety_allowance(cfg, srules, light, level, weather, fall):
    profile = UserProfile(signup_date=D0, fall_concern=fall, goal="시장 걸어가기")
    steps = cfg["ladder"]["steps_minutes"]
    for h in _histories():
        plan = plan_today(cfg, srules, profile, LadderState(level, D0), h, decision(srules, light), day(20), weather)
        allowed = allowance(srules, light, steps[level])
        if plan.action != "EXERCISE":
            assert plan.action == "DONE_FOR_TODAY" and plan.minutes == 0
            continue
        assert plan.minutes <= allowed["max_minutes"]
        assert plan.minutes <= 60
        activity = cfg.activity(plan.activity_id)
        if allowed["intensity"] == "low":
            assert activity["intensity"] == "low"
        if weather:
            assert activity["indoor"]
        if fall:
            assert activity["supported"]
        assert plan.easier["minutes"] < plan.minutes
        assert cfg.activity(plan.easier["activity_id"])["intensity"] == "low"


def test_yellow_halves_and_explains(cfg, srules):
    h = hist([sess(i, level=3) for i in range(5, 18, 2)])
    green = plan_today(cfg, srules, ME, LadderState(3, D0), h, decision(srules, "GREEN"), day(18))
    yellow = plan_today(cfg, srules, ME, LadderState(3, D0), h, decision(srules, "YELLOW"), day(18))
    assert (green.minutes, yellow.minutes) == (10, 5)
    assert yellow.intensity == "low" and yellow.message.intent == "today_yellow" and "R03" in yellow.rules_fired


def test_fear_state_starts_seated_three_minutes(cfg, srules):
    plan = plan_today(cfg, srules, ME, LadderState(0, D0), hist(), decision(srules, "GREEN"), day(1))
    assert plan.minutes == 3 and cfg.activity(plan.activity_id)["seated"] and plan.easier["minutes"] == 1
    assert plan.state == "FEAR" and "R04" in plan.rules_fired


def test_slow_recovery_lowers_next_intensity(cfg, srules):
    base = [sess(i, level=3) for i in range(5, 16, 2)]
    h_ok = hist(base + [sess(17, level=3)])
    h_slow = hist(base + [sess(17, level=3, slow_recovery=True)])
    assert plan_today(cfg, srules, ME, LadderState(3, D0), h_ok, decision(srules, "GREEN"), day(18)).intensity == "moderate"
    assert plan_today(cfg, srules, ME, LadderState(3, D0), h_slow, decision(srules, "GREEN"), day(18)).intensity == "low"


def test_daily_cap_reached(cfg, srules):
    h = hist([sess(20, level=6, minutes=30), sess(20, level=6, minutes=28)])
    plan = plan_today(cfg, srules, ME, LadderState(6, D0), h, decision(srules, "GREEN"), day(20))
    assert plan.action == "DONE_FOR_TODAY" and "R07" in plan.rules_fired


def test_weather_message_explains_reason(cfg, srules):
    plan = plan_today(cfg, srules, ME, LadderState(0, D0), hist(), decision(srules, "GREEN"), day(1),
                      Weather(pm25=50))
    assert plan.message.intent == "today_weather" and "미세먼지" in plan.message.text


def test_completion_uses_goal(cfg):
    with_goal = completion_message(cfg, UserProfile(signup_date=D0, goal="손주 안아주기"), hist(), day(1))
    assert "손주 안아주기" in with_goal.text
    assert completion_message(cfg, ME, hist(), day(1)).intent == "complete"


def test_level_down_message_not_failure(cfg):
    m = ladder_message(cfg, hist(), day(1), LadderState(1, day(1)), "LADDER_DOWN_SAFETY")
    assert m.intent == "level_down" and "5분" in m.text and "실패" not in m.text
    assert ladder_message(cfg, hist(), day(1), LadderState(1, day(1)), "LADDER_HOLD") is None


# ---- 재참여 (R15) ----
FULL = UserProfile(signup_date=D0, guardian_mode="full", consent_guardian_cheer_request=True,
                   has_guardian_cheer=True, manager_linked=True, consent_manager=True)


@pytest.mark.parametrize("today,tier,actions", [
    (2, None, []),                                                      # 하루 미실행
    (3, "MISSED_2", ["ask_reason"]),
    (4, "MISSED_3", ["play_guardian_cheer", "request_guardian_cheer"]),
    (5, "MISSED_3", []),                                                # 단계 진입 날에만
    (6, "MISSED_5", ["cause_check", "guardian_weekly_summary"]),
    (10, "MISSED_5", []),
    (15, "MISSED_14", ["restart_offer", "guardian_lapse_alert", "manager_call"]),
])
def test_reengagement_ladder(cfg, today, tier, actions):
    r = reengagement(cfg, FULL, hist([sess(0)]), day(today))
    assert (r["tier"], r["actions"]) == (tier, actions)


def test_reengagement_respects_consent(cfg):
    cheer_only = UserProfile(signup_date=D0, guardian_mode="cheer_only", has_guardian_cheer=True)
    r3 = reengagement(cfg, cheer_only, hist([sess(0)]), day(4))
    assert r3["actions"] == ["play_guardian_cheer"] and r3["withheld"] == ["request_guardian_cheer"]
    r5 = reengagement(cfg, cheer_only, hist([sess(0)]), day(6))
    assert "guardian_weekly_summary" in r5["withheld"]
    r14 = reengagement(cfg, UserProfile(signup_date=D0), hist([sess(0)]), day(15))
    assert r14["actions"] == ["restart_offer"]
    assert set(r14["withheld"]) == {"guardian_lapse_alert", "manager_call"}


# ---- 보상 (R16) ----
def test_reward_for_start_bp_and_red_rest_not_amount(cfg):
    assert day_reward(hist([sess(1, minutes=3)]), day(1)) == day_reward(hist([sess(1, minutes=30)]), day(1))
    assert day_reward(hist([sess(1, completed=False, minutes=1)]), day(1))["stamp"]   # 시작만 해도
    red = day_reward(hist(prechecks=[PrecheckRecord(day(1), "RED")]), day(1))
    assert red == {"stamp": True, "reasons": ["BP_MEASURED", "RESTED_ON_RED"]}
    assert day_reward(hist(), day(1)) == {"stamp": False, "reasons": []}


def test_streak_and_weekly(cfg):
    h = hist([sess(i) for i in (3, 4, 5)], [PrecheckRecord(day(6), "RED")])
    assert streak(h, day(6)) == 4
    assert streak(h, day(7)) == 4          # 오늘 아직 안 했어도 끊지 않음
    assert streak(h, day(8)) == 0
    assert weekly_stamps(h, day(7)) == 4
