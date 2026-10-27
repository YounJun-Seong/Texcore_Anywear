import pytest
from sqlalchemy import text

from app import models as m
from app.engines import verify_log


def test_green_day_full_loop(w):
    h, uid = w.elder(settings={"goal": "손주 안아주기", "preferred_time": "09:00"})
    today = w.client.get("/me/today", headers=h).json()
    assert today["state"] == "FEAR" and today["ladder"]["minutes"] == 3

    pre = w.precheck(h)
    assert pre["outcome"] == "GREEN"
    plan = pre["plan"]
    assert plan["action"] == "EXERCISE" and plan["minutes"] == 3 and plan["easier"]["minutes"] == 1
    assert "{" not in plan["message"]["text"]

    s = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h).json()
    # 1952년생 → 74세: 최대 심박 208-0.7×74=156.2, 시작 4주 70% → 109
    assert s["hr_limits"]["ceiling"] == 109 and s["minutes"] == 3
    done = w.client.post(f"/me/sessions/{s['session_id']}/finish", json={"completed": True, "minutes": 3},
                         headers=h).json()
    assert "손주 안아주기" in done["message"]
    assert done["rewards"]["today"]["stamp"] and done["rewards"]["streak"] == 1


def test_red_day_rest_and_stamp_no_session(w):
    h, _ = w.elder()
    pre = w.precheck(h, sbp=185)
    assert pre["outcome"] == "RED" and pre["plan"]["action"] == "REST_AND_PRAISE"
    r = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h)
    assert r.status_code == 409
    rewards = w.client.get("/me/today", headers=h).json()["rewards"]["today"]
    assert rewards == {"stamp": True, "reasons": ["BP_MEASURED", "RESTED_ON_RED"]}


def test_yellow_shortens_and_caps_hr(w):
    h, _ = w.elder()
    with w.ctx.sessionmaker() as db:
        p = db.get(m.ElderProfile, 1)
        p.ladder_level = 3          # 10분 단계
        db.commit()
    pre = w.precheck(h, sbp=165)
    assert pre["outcome"] == "YELLOW" and pre["plan"]["minutes"] == 5
    s = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h).json()
    assert s["hr_limits"]["ceiling_pct"] == 0.64


def test_session_rules_enforced_server_side(w):
    h, _ = w.elder()
    pre = w.precheck(h)
    s = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h).json()
    too_long = w.client.post(f"/me/sessions/{s['session_id']}/finish", json={"completed": True, "minutes": 30},
                             headers=h)
    assert too_long.status_code == 422
    w.client.post(f"/me/sessions/{s['session_id']}/finish", json={"completed": True, "minutes": 3}, headers=h)
    again = w.client.post(f"/me/sessions/{s['session_id']}/finish", json={"completed": True, "minutes": 3}, headers=h)
    assert again.status_code == 409
    # 어제 점검으로는 오늘 운동 못 함
    w.at(days=1)
    r = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h)
    assert r.status_code == 409
    # 남의 기록
    other, _ = w.elder(phone="01099998888")
    assert w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=other).status_code == 404


def test_easier_option(w):
    h, _ = w.elder()
    pre = w.precheck(h)
    s = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"], "easier": True}, headers=h).json()
    assert s["minutes"] == 1


def test_unknown_symptom_rejected(w):
    h, _ = w.elder()
    r = w.client.post("/me/prechecks", json={"systolic": 130, "diastolic": 80, "resting_hr": 70,
                                             "symptoms": ["headache"]}, headers=h)
    assert r.status_code == 422


def test_hard_gate_blocks(w):
    h, _ = w.elder(health={"parq_risk": True})
    pre = w.precheck(h)
    assert pre["outcome"] == "BLOCKED" and pre["plan"]["action"] == "DOCTOR_CHECK"


def test_slow_recovery_recorded(w):
    h, _ = w.elder()
    _, _, done = w.exercise(h, resting_hr=70, hr_after_recovery=95)
    assert done["slow_recovery"] is True


# ---- 응급 ----
def test_emergency_symptom_alerts_every_guardian_scope(w):
    h, uid = w.elder()
    g1, gid1 = w.guardian(h, phone="01033334444", scope="emergency_only")
    g2, gid2 = w.guardian(h, phone="01055556666", scope="full")
    pre = w.precheck(h, symptoms=["chest_pain"])
    assert pre["outcome"] == "EMERGENCY" and pre["guardians_alerted"] == 2
    for gid in (gid1, gid2):
        assert any(s.channel == "call" and s.to_user_id == gid for s in w.gw.sent)
        assert w.pushes(gid, "emergency")


def test_emergency_location_only_with_consent_and_never_stored(w):
    h, uid = w.elder()
    g, gid = w.guardian(h)
    loc = {"lat": 37.34, "lng": 126.97}
    r = w.client.post("/me/emergency", json={"code": "EM_USER_NOT_OK", "location": loc}, headers=h).json()
    assert r["location_sent"] is False
    assert "location" not in w.pushes(gid, "emergency")[-1].data

    w.client.post("/me/consents", json={"kind": "location", "granted": True}, headers=h)
    r = w.client.post("/me/emergency", json={"code": "EM_119_CONFIRMED", "severe": True, "location": loc},
                      headers=h).json()
    assert r["location_sent"] is True
    assert w.pushes(gid, "emergency")[-1].data["location"] == loc
    with w.ctx.sessionmaker() as db:
        dump = str([a.payload for a in db.query(m.GuardianAlert)]) + str([r.payload for r in db.query(m.DecisionLogRow)])
    assert "37.34" not in dump and "126.97" not in dump


def test_device_no_response_event_alerts_guardian(w):
    h, uid = w.elder()
    g, gid = w.guardian(h, scope="emergency_only")
    pre = w.precheck(h)
    s = w.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h).json()
    events = [{"t": 31, "event": "hr", "value": 115, "actions": [{"kind": "SLOW_DOWN", "code": "HR_OVER_CEILING"}]},
              {"t": 180, "event": "tick", "actions": [{"kind": "GUARDIAN_ALERT", "code": "NO_RESPONSE"},
                                                      {"kind": "LOUD_PROMPT", "code": "NO_RESPONSE"}]}]
    r = w.client.post(f"/me/sessions/{s['session_id']}/events", json={"events": events}, headers=h).json()
    assert r == {"stored": 2, "guardians_alerted": 1}
    assert w.pushes(gid, "no_response")


# ---- 판정 로그 ----
def test_decision_log_chain_and_tamper_detection(w):
    h, uid = w.elder()
    w.exercise(h)
    w.precheck(h, sbp=185)
    with w.ctx.sessionmaker() as db:
        kinds = [r.kind for r in db.query(m.DecisionLogRow).order_by(m.DecisionLogRow.seq)]
        assert kinds.count("pre_check") == 2 and "session_start" in kinds
        assert verify_log(db) == (True, None)
        row = db.query(m.DecisionLogRow).filter_by(kind="pre_check").first()
        row.payload = {**row.payload, "outcome": "GREEN"}
        with pytest.raises(m.ImmutableRowError):
            db.commit()
        db.rollback()
        # ORM을 우회한 직접 수정도 체인 검증에서 걸린다
        db.execute(text("UPDATE decision_log SET payload = '{}' WHERE seq = 1"))
        db.commit()
        assert verify_log(db) == (False, 1)
