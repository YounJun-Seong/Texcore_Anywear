"""휴대폰 본인인증(문자 코드) + 간편 로그인 토큰. 아이디·비밀번호 없음(3장)."""
import re
import secrets
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models as m
from ..deps import AppContext, ctx, get_db, hash_secret
from ..engines import _as_aware
from ..gateway import Outbound

router = APIRouter(prefix="/auth", tags=["auth"])


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if not 10 <= len(digits) <= 11:
        raise HTTPException(422, "휴대폰 번호를 확인해 주세요")
    return digits


def issue_token(db: Session, c: AppContext, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db.add(m.AuthToken(token_hash=hash_secret(token), user_id=user_id,
                       expires_at=c.clock.now() + timedelta(days=c.settings.token_ttl_days)))
    return token


def create_elder(db: Session, c: AppContext, phone, name, birth_year, proxy=False):
    today = c.clock.today()
    user = m.User(role="elder", phone=phone, name=name, created_at=c.clock.now())
    db.add(user)
    db.flush()
    db.add(m.ElderProfile(user_id=user.id, birth_year=birth_year, signup_date=today, proxy_setup=proxy,
                          ladder_last_change=today))
    return user


class OtpRequest(BaseModel):
    phone: str


class OtpVerify(BaseModel):
    phone: str
    code: str
    # 처음 가입할 때만
    role: Literal["elder", "guardian"] | None = None
    name: str | None = Field(None, max_length=64)
    birth_year: int | None = Field(None, ge=1900, le=2010)


@router.post("/otp/request")
def request_otp(body: OtpRequest, db: Session = Depends(get_db), c: AppContext = Depends(ctx)):
    phone = normalize_phone(body.phone)
    code = f"{secrets.randbelow(10**6):06d}"
    db.add(m.OtpCode(phone=phone, code_hash=hash_secret(f"{phone}:{code}"),
                     expires_at=c.clock.now() + timedelta(seconds=c.settings.otp_ttl_seconds)))
    c.gateway.send(Outbound("sms", None, phone, "인증번호", f"[운동친구] 인증번호 {code}", {"code": code}))
    return {"sent": True, "expires_in": c.settings.otp_ttl_seconds}


@router.post("/otp/verify")
def verify_otp(body: OtpVerify, db: Session = Depends(get_db), c: AppContext = Depends(ctx)):
    phone = normalize_phone(body.phone)
    otp = db.execute(select(m.OtpCode).where(m.OtpCode.phone == phone, m.OtpCode.used.is_(False))
                     .order_by(m.OtpCode.id.desc())).scalars().first()
    if otp is None or _as_aware(otp.expires_at) < c.clock.now() or otp.attempts >= c.settings.otp_max_attempts:
        raise HTTPException(400, "인증번호를 다시 받아 주세요")
    if otp.code_hash != hash_secret(f"{phone}:{body.code}"):
        otp.attempts += 1
        db.commit()
        raise HTTPException(400, "인증번호가 맞지 않아요")
    otp.used = True

    user = db.execute(select(m.User).where(m.User.phone == phone)).scalar_one_or_none()
    if user is None:
        if body.role is None or not body.name:
            raise HTTPException(422, "처음 오셨네요. 이름과 사용자 종류가 필요해요")
        if body.role == "elder":
            if body.birth_year is None:
                raise HTTPException(422, "태어난 해가 필요해요")
            user = create_elder(db, c, phone, body.name, body.birth_year)
        else:
            user = m.User(role="guardian", phone=phone, name=body.name, created_at=c.clock.now())
            db.add(user)
            db.flush()
    return {"token": issue_token(db, c, user.id), "user": {"id": user.id, "role": user.role, "name": user.name}}
