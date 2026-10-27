import json

from safety_engine import Profile, SafetyEngine, Vitals
from safety_engine.audit_log import DecisionLog


def test_engine_logs_every_decision_with_rule_version(tmp_path, rules):
    log = DecisionLog(tmp_path / "decisions.jsonl")
    eng = SafetyEngine(rules, log)
    p = Profile(age=70)
    eng.hard_gate(p)
    eng.pre_check(p, Vitals(165, 85, 72), symptoms=["mild_fatigue"])
    _, mon = eng.start_session(p, "A")
    for t in range(0, 35):
        mon.on_hr(t, 115)
    eng.start_emergency(40, severe=False, snapshot={"hr": 115})

    recs = [json.loads(line) for line in (tmp_path / "decisions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [r["kind"] for r in recs] == ["hard_gate", "pre_check", "session_start", "session_event", "emergency_start"]
    pre = recs[1]
    assert pre["payload"]["outcome"] == "YELLOW"
    assert pre["payload"]["inputs"]["vitals"]["systolic"] == 165
    assert "PRE_SBP_ELEVATED" in pre["payload"]["reasons"]
    assert all(r["rule_version"] == rules.version and r["rule_sha256"] == rules.sha256 for r in recs)
    assert recs[3]["payload"]["actions"][0]["code"] == "HR_OVER_CEILING"
    assert log.verify() == (True, None)


def test_tampering_detected(tmp_path, rules):
    path = tmp_path / "decisions.jsonl"
    eng = SafetyEngine(rules, DecisionLog(path))
    for sbp in (120, 170, 190):
        eng.pre_check(Profile(age=70), Vitals(sbp, 80, 70))

    lines = path.read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[1])
    rec["payload"]["outcome"] = "GREEN"   # 노랑을 초록으로 몰래 고침
    lines[1] = json.dumps(rec, ensure_ascii=False)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert DecisionLog(path).verify() == (False, 1)


def test_deleted_line_detected(tmp_path, rules):
    path = tmp_path / "decisions.jsonl"
    eng = SafetyEngine(rules, DecisionLog(path))
    for sbp in (120, 170, 190):
        eng.pre_check(Profile(age=70), Vitals(sbp, 80, 70))
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join([lines[0], lines[2]]) + "\n", encoding="utf-8")
    assert DecisionLog(path).verify() == (False, 1)


def test_reopen_continues_chain(tmp_path, rules):
    path = tmp_path / "decisions.jsonl"
    SafetyEngine(rules, DecisionLog(path)).pre_check(Profile(age=70), Vitals(120, 80, 70))
    log2 = DecisionLog(path)
    SafetyEngine(rules, log2).pre_check(Profile(age=70), Vitals(170, 80, 70))
    assert log2.verify() == (True, None)
    assert log2.seq == 2
