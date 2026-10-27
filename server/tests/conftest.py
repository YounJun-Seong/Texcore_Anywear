from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app import models as m
from app.config import KST, FixedClock, Settings
from app.gateway import MemoryGateway
from app.main import create_app

START = datetime(2026, 11, 2, 8, 0, tzinfo=KST)   # 월요일 아침


class World:
    def __init__(self, allow_draft=True):
        self.clock = FixedClock(START)
        self.gw = MemoryGateway()
        self.app = create_app(Settings(database_url="sqlite://", allow_draft_rules=allow_draft), self.clock, self.gw)
        self.client = TestClient(self.app)
        self.ctx = self.app.state.ctx

    # ---- 시간 ----
    def at(self, days=0, hour=8, minute=0):
        self.clock.set(START.replace(hour=hour, minute=minute) + timedelta(days=days))

    # ---- 로그인 ----
    def login(self, phone, role="elder", name="김영자", birth_year=1952):
        self.client.post("/auth/otp/request", json={"phone": phone})
        digits = "".join(ch for ch in phone if ch.isdigit())
        code = [s for s in self.gw.sent if s.channel == "sms" and s.to_phone == digits][-1].data["code"]
        r = self.client.post("/auth/otp/verify", json={"phone": phone, "code": code, "role": role, "name": name,
                                                      "birth_year": birth_year})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['token']}"}, r.json()["user"]["id"]

    def admin(self):
        with self.ctx.sessionmaker() as db:
            db.add(m.User(role="admin", phone="01000000000", name="관리자", created_at=START))
            db.commit()
        return self.login("01000000000")[0]

    # ---- 어르신 준비 ----
    def elder(self, phone="01011112222", health=None, settings=None):
        h, uid = self.login(phone)
        assert self.client.post("/me/consents", json={"kind": "health", "granted": True}, headers=h).status_code == 200
        r = self.client.put("/me/health", json=health or {}, headers=h)
        assert r.status_code == 200, r.text
        if settings:
            self.client.put("/me/settings", json=settings, headers=h)
        return h, uid

    def guardian(self, elder_h, phone="01033334444", scope="full", name="이지은"):
        g, gid = self.login(phone, role="guardian", name=name)
        elder_phone = self.client.get("/me", headers=elder_h).json()
        with self.ctx.sessionmaker() as db:
            ephone = db.get(m.User, elder_phone["id"]).phone
        link = self.client.post("/guardian/links", json={"elder_phone": ephone}, headers=g).json()
        r = self.client.put(f"/me/guardians/{link['link_id']}", json={"status": "active", "scope": scope},
                            headers=elder_h)
        assert r.status_code == 200
        return g, gid

    def precheck(self, h, sbp=130, dbp=80, hr=70, **kw):
        r = self.client.post("/me/prechecks", json={"systolic": sbp, "diastolic": dbp, "resting_hr": hr, **kw},
                             headers=h)
        assert r.status_code == 200, r.text
        return r.json()

    def exercise(self, h, completed=True, **finish):
        pre = self.precheck(h)
        s = self.client.post("/me/sessions", json={"precheck_id": pre["precheck_id"]}, headers=h).json()
        body = {"completed": completed, "minutes": s["minutes"], **finish}
        r = self.client.post(f"/me/sessions/{s['session_id']}/finish", json=body, headers=h)
        assert r.status_code == 200, r.text
        return pre, s, r.json()

    def pushes(self, user_id, kind=None):
        return [s for s in self.gw.sent if s.to_user_id == user_id and s.channel == "push"
                and (kind is None or s.data.get("kind") == kind)]


@pytest.fixture
def w():
    return World()
