from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def make_engine(url):
    if url.startswith("sqlite"):
        kw = {"connect_args": {"check_same_thread": False}}
        if url in ("sqlite://", "sqlite:///:memory:"):
            kw["poolclass"] = StaticPool
        return create_engine(url, **kw)
    return create_engine(url, pool_pre_ping=True)


def make_sessionmaker(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
