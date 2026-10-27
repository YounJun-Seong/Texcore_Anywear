import copy

import pytest

from safety_engine.rules import RuleError, bundle_from_dict, load_rules
from scenario_runner import SUITES, load_suite


def _mutated(rules, fn):
    data = copy.deepcopy(rules.data)
    fn(data)
    return bundle_from_dict(data)


def _failures(bundle):
    bad = []
    for name in SUITES:
        rows, runner = load_suite(name)
        bad += [row["id"] for row in rows if not runner(bundle, row)[0]]
    return bad


def test_hash_is_stable_and_content_based(rules):
    again = load_rules()
    assert again.sha256 == rules.sha256
    changed = _mutated(rules, lambda d: d["session"]["rpe"].update(step_down_at=13))
    assert changed.sha256 != rules.sha256


@pytest.mark.parametrize("mutation", [
    lambda d: d["precheck"]["bands"]["systolic"][2].update(lower=165) or d["precheck"]["bands"]["systolic"][1].update(upper=165),
    lambda d: d["precheck"]["bands"]["resting_hr"][1].update(light="GREEN"),
    lambda d: d["session"]["ceiling_pct"].update(initial=0.72),
    lambda d: d["session"]["rpe"].update(stop_at=17),
    lambda d: d["session"].update(no_response_seconds=240),
    lambda d: d["emergency"].update(ask_ok_timeout_seconds=90),
    lambda d: d["precheck"]["red_symptoms"].remove("dizziness") or d["precheck"]["yellow_symptoms"].append("dizziness"),
])
def test_unapproved_threshold_change_breaks_answer_table(rules, mutation):
    """규칙 수치를 바꾸면 정답표가 깨져야 한다 = 자문단 승인 없는 변경이 조용히 지나가지 않는다."""
    assert _failures(_mutated(rules, mutation))


@pytest.mark.parametrize("mutation,msg", [
    (lambda d: d["precheck"]["bands"]["systolic"][1].update(upper=158), "gap"),
    (lambda d: d["precheck"]["bands"]["diastolic"][0].update(lower=0), "first band"),
    (lambda d: d["session"]["ceiling_pct"].update(absolute_max=0.9), "ceiling_pct"),
    (lambda d: d["session"]["ceiling_pct"].update(initial=0.8), "ceiling_pct"),
    (lambda d: d["allowance"]["RED"].update(allowed=True), "RED"),
    (lambda d: d["session"]["rpe"].update(step_down_at=16), "rpe"),
    (lambda d: d["precheck"]["yellow_symptoms"].append("chest_pain"), "overlap"),
    (lambda d: d["meta"].update(status="approved"), "approved_by"),
    (lambda d: d["session"]["sensor"].update(fallback_checkin_interval_seconds=300), "fallback"),
    (lambda d: d.pop("emergency"), "emergency"),
])
def test_invalid_bundles_rejected(rules, mutation, msg):
    with pytest.raises(RuleError, match=msg):
        _mutated(rules, mutation)


def test_draft_bundle_refused_when_approval_required():
    with pytest.raises(RuleError, match="not approved"):
        load_rules(require_approved=True)


def test_approved_bundle_loads(rules):
    def approve(d):
        d["meta"].update(status="approved", approved_by=[{"name": "자문의", "role": "순환기내과", "date": "2026-11-01"}])
    data = copy.deepcopy(rules.data)
    approve(data)
    assert bundle_from_dict(data, require_approved=True).approved


def test_device_bundle_json_roundtrip(rules):
    import json
    assert bundle_from_dict(json.loads(rules.to_json())).sha256 == rules.sha256
