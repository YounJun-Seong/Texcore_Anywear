from app import models as m


def test_link_needs_elder_approval_and_starts_emergency_only(w):
    h, uid = w.elder()
    g, gid = w.login("01033334444", role="guardian", name="딸")
    link = w.client.post("/guardian/links", json={"elder_phone": "010-1111-2222"}, headers=g).json()
    assert link["status"] == "pending"
    assert w.client.get(f"/guardian/elders/{uid}/summary", headers=g).status_code == 404
    w.client.put(f"/me/guardians/{link['link_id']}", json={"status": "active"}, headers=h)
    s = w.client.get(f"/guardian/elders/{uid}/summary", headers=g).json()
    assert s["scope"] == "emergency_only" and "done_today" not in s and s["can_cheer"] is False


def test_summary_respects_scope(w):
    h, uid = w.elder()
    full, _ = w.guardian(h, phone="01033334444", scope="full")
    cheer, _ = w.guardian(h, phone="01055556666", scope="cheer_only")
    w.exercise(h)
    s_full = w.client.get(f"/guardian/elders/{uid}/summary", headers=full).json()
    s_cheer = w.client.get(f"/guardian/elders/{uid}/summary", headers=cheer).json()
    assert s_full["done_today"] is True and s_full["week"]["sessions"] == 1
    assert "done_today" not in s_cheer and "week" not in s_cheer and s_cheer["can_cheer"]
    with w.ctx.sessionmaker() as db:
        assert db.query(m.AccessLog).filter_by(elder_id=uid).count() == 2


def test_daily_done_only_to_full_scope(w):
    h, uid = w.elder()
    full, gfull = w.guardian(h, phone="01033334444", scope="full")
    cheer, gcheer = w.guardian(h, phone="01055556666", scope="cheer_only")
    w.exercise(h)
    assert len(w.pushes(gfull, "daily_done")) == 1
    assert w.pushes(gcheer, "daily_done") == []
    assert [a["kind"] for a in w.client.get("/guardian/alerts", headers=cheer).json()] == []


def test_elder_can_revoke(w):
    h, uid = w.elder()
    g, gid = w.guardian(h)
    link_id = w.client.get("/me/guardians", headers=h).json()[0]["link_id"]
    w.client.put(f"/me/guardians/{link_id}", json={"status": "revoked"}, headers=h)
    assert w.client.get(f"/guardian/elders/{uid}/summary", headers=g).status_code == 404
    w.precheck(h, symptoms=["chest_pain"])
    assert w.pushes(gid) == []


def test_cheer_flow(w):
    h, uid = w.elder()
    emerg, _ = w.guardian(h, phone="01077778888", scope="emergency_only")
    g, gid = w.guardian(h, scope="cheer_only", name="이지은")
    assert w.client.post(f"/guardian/elders/{uid}/cheers", json={"text": "엄마 화이팅"}, headers=emerg).status_code == 403
    assert w.client.post(f"/guardian/elders/{uid}/cheers", json={}, headers=g).status_code == 422
    w.client.post(f"/guardian/elders/{uid}/cheers", json={"text": "엄마 오늘도 응원해요",
                                                         "audio_url": "https://cdn.example/c1.m4a"}, headers=g)
    assert w.client.get("/me/today", headers=h).json()["has_new_cheer"] is True
    _, _, done = w.exercise(h)
    assert done["cheer"] == {"from": "이지은", "text": "엄마 오늘도 응원해요", "audio_url": "https://cdn.example/c1.m4a"}
    _, _, again = w.exercise(h)
    assert again["cheer"] is None


def test_guardian_cannot_see_other_elders(w):
    h1, uid1 = w.elder(phone="01011112222")
    h2, uid2 = w.elder(phone="01022223333")
    g, _ = w.guardian(h1)
    assert w.client.get(f"/guardian/elders/{uid2}/summary", headers=g).status_code == 404
    assert w.client.post(f"/guardian/elders/{uid2}/cheers", json={"text": "x"}, headers=g).status_code == 404


def test_proxy_setup(w):
    g, gid = w.login("01033334444", role="guardian", name="복지사")
    r = w.client.post("/guardian/elders", json={
        "phone": "01044445555", "name": "박순철", "birth_year": 1958, "consent_health": True,
        "health": {"beta_blocker": True}, "settings": {"preferred_time": "10:00", "fall_concern": True}}, headers=g)
    assert r.status_code == 200, r.text
    eid = r.json()["elder_id"]
    assert r.json()["scope"] == "emergency_only"
    with w.ctx.sessionmaker() as db:
        consent = db.query(m.Consent).filter_by(elder_id=eid).one()
        assert consent.actor_id == gid                    # 누가 대신 동의했는지 남는다
        p = db.get(m.ElderProfile, eid)
        assert p.proxy_setup and p.health["beta_blocker"] and p.fall_concern
    assert w.client.put(f"/guardian/elders/{eid}/health", json={"beta_blocker": False}, headers=g).status_code == 200
    # 어르신 본인은 자기 번호로 로그인해 바로 쓴다
    h, uid = w.login("01044445555")
    assert uid == eid and w.precheck(h)["outcome"] == "GREEN"
    # 이미 있는 번호로 대리 가입 불가
    dup = w.client.post("/guardian/elders", json={"phone": "01044445555", "name": "x", "birth_year": 1950,
                                                   "consent_health": True}, headers=g)
    assert dup.status_code == 409


def test_no_proxy_health_edit_for_self_registered_elder(w):
    h, uid = w.elder()
    g, _ = w.guardian(h)
    assert w.client.put(f"/guardian/elders/{uid}/health", json={}, headers=g).status_code == 403
