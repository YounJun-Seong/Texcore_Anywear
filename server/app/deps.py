import hashlib
from dataclasses import dataclass, field
from typing import Callable

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from . import models as m
from .config import Clock, Settings
from .engines import Engines, _as_aware
from .gateway import Gateway


@dataclass
class AppContext:
    settings: Settings
    sessionmaker: object
    clock: Clock
    engines: Engines
    gateway: Gateway
    # 날씨 공공 API(기상청·에어코리아) 연결부. 없으면 날씨 전환 없이 계획한다.
    weather: Callable = field(default=lambda elder_id, day: None)


def ctx(request: Request) -> AppContext:
    return request.app.state.ctx


def get_db(c: AppContext = Depends(ctx)):
    db: Session = c.sessionmaker()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def hash_secret(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


_bearer = HTTPBearer(auto_error=False)


def current_user(cred: HTTPAuthorizationCredentials | None = Depends(_bearer), db: Session = Depends(get_db),
                 c: AppContext = Depends(ctx)) -> m.User:
    if cred is None:
        raise HTTPException(401, "로그인이 필요해요")
    tok = db.get(m.AuthToken, hash_secret(cred.credentials))
    if tok is None or _as_aware(tok.expires_at) < c.clock.now():
        raise HTTPException(401, "다시 로그인해 주세요")
    user = db.get(m.User, tok.user_id)
    if user is None or not user.active:
        raise HTTPException(401, "사용할 수 없는 계정이에요")
    return user


def role(*roles):
    def check(user: m.User = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(403, "권한이 없어요")
        return user
    return check


elder_user = role("elder")
guardian_user = role("guardian")
admin_user = role("admin")
