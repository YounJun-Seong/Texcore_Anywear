from fastapi import FastAPI

from .config import Clock, Settings
from .db import Base, make_engine, make_sessionmaker
from .deps import AppContext
from .engines import Engines
from .gateway import MemoryGateway
from .routers import admin, auth, daily, guardian, me, rules


def create_app(settings: Settings | None = None, clock: Clock | None = None, gateway=None, engines=None,
               weather=None) -> FastAPI:
    settings = settings or Settings()
    engine = make_engine(settings.database_url)
    # 개발·테스트용. 운영은 마이그레이션 도구(Alembic)로 스키마를 관리하고
    # decision_log에는 UPDATE/DELETE 권한을 주지 않는다.
    Base.metadata.create_all(engine)
    app = FastAPI(title="어르신 운동 코치 서버", version="0.1.0")
    app.state.ctx = AppContext(settings=settings, sessionmaker=make_sessionmaker(engine), clock=clock or Clock(),
                               engines=engines or Engines(), gateway=gateway or MemoryGateway())
    if weather is not None:
        app.state.ctx.weather = weather
    for r in (auth, me, daily, guardian, rules, admin):
        app.include_router(r.router)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app
