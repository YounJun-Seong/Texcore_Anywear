"""정답표가 빠뜨린 값까지 훑는 성질 검사: 값이 나빠지면 판정은 절대 좋아지지 않는다."""
import itertools

import pytest

from safety_engine.codes import SEVERITY, Light
from safety_engine.precheck import pre_check
from safety_engine.session import SessionMonitor, hr_limits
from safety_engine.types import DoctorLimits, Profile, Vitals

P = Profile(age=72)
BASE = dict(systolic=130, diastolic=70, resting_hr=70)


def sev(rules, profile=P, symptoms=(), conditions=(), **kw):
    v = dict(BASE, **kw)
    return SEVERITY[Light(pre_check(rules, profile, Vitals(**v), symptoms, conditions).outcome)]


@pytest.mark.parametrize("metric,normal,lo,hi", [
    ("systolic", 130, 71, 259),
    ("diastolic", 70, 31, 129),
    ("resting_hr", 70, 31, 219),
])
def test_moving_away_from_normal_never_improves(rules, metric, normal, lo, hi):
    for direction in (range(normal, hi + 1), range(normal, lo - 1, -1)):
        prev = -1
        for v in direction:
            s = sev(rules, **{metric: v})
            assert s >= prev, f"{metric}={v} improved the light"
            prev = s


def test_never_green_outside_green_bands(rules):
    for sbp, dbp, hr in itertools.product(range(70, 261, 5), range(30, 151, 5), range(30, 221, 5)):
        if sev(rules, systolic=sbp, diastolic=dbp, resting_hr=hr) == 0:
            assert 90 <= sbp < 160 and 50 <= dbp < 100 and 50 <= hr < 100 and sbp > dbp


@pytest.mark.parametrize("extra", [
    {"symptoms": ["mild_fatigue"]}, {"symptoms": ["dizziness"]}, {"conditions": ["poor_sleep"]},
    {"conditions": ["fever"]}, {"profile": Profile(age=72, doctor_limits=DoctorLimits(systolic_max=140))},
])
def test_adding_risk_never_improves(rules, extra):
    for sbp in range(80, 200, 7):
        assert sev(rules, systolic=sbp, **extra) >= sev(rules, systolic=sbp)


def test_looser_doctor_limit_never_relaxes(rules):
    loose = Profile(age=72, doctor_limits=DoctorLimits(systolic_max=220, diastolic_max=130, resting_hr_max=150))
    for sbp, hr in itertools.product(range(80, 260, 5), range(35, 220, 5)):
        assert sev(rules, loose, systolic=sbp, resting_hr=hr) == sev(rules, systolic=sbp, resting_hr=hr)


def test_unknown_inputs_rejected(rules):
    with pytest.raises(ValueError):
        pre_check(rules, P, Vitals(130, 70, 70), symptoms=["chestpain"])
    with pytest.raises(ValueError):
        pre_check(rules, P, Vitals(130, 70, 70), conditions=["cold"])
    with pytest.raises(ValueError):
        pre_check(rules, Profile(age=72, conditions=frozenset({"angina"})), Vitals(130, 70, 70))
    with pytest.raises(ValueError):
        pre_check(rules, P, Vitals(130, 70, 70, bp_source="wrist"))


def test_ceiling_never_exceeds_85_percent(rules):
    for age in range(50, 100):
        for weeks, esc, beta in itertools.product((0, 4, 12), (False, True), (False, True)):
            lim = hr_limits(rules, Profile(age=age, beta_blocker=beta), weeks, esc)
            assert lim["ceiling"] <= (208 - 0.7 * age) * 0.85


def test_pacemaker_without_ceiling_refused(rules):
    with pytest.raises(ValueError):
        hr_limits(rules, Profile(age=70, device="pacemaker"))


def test_session_rejects_time_going_backwards(rules):
    m = SessionMonitor(rules, 111, "A")
    m.on_hr(10, 100)
    with pytest.raises(ValueError):
        m.on_hr(9, 100)


def test_session_rejects_bad_rpe_and_symptom(rules):
    m = SessionMonitor(rules, 111, "A")
    with pytest.raises(ValueError):
        m.on_rpe(1, 25)
    with pytest.raises(ValueError):
        m.on_symptom(2, "headache")
