"""운영 명령. cron(또는 클라우드 스케줄러)에서 부른다.

    python -m app.cli daily              # 매일 06:30: 사다리·오늘 알림 예약·재참여
    python -m app.cli dispatch           # 매 5분: 예약 시각이 지난 알림 발송
    python -m app.cli create-admin 01012345678 관리자
"""
import sys

from .config import Clock, Settings
from .db import Base, make_engine, make_sessionmaker
from .deps import AppContext
from .engines import Engines
from .gateway import MemoryGateway
from . import models as m
from .services import dispatch_due, run_daily


def main(argv):
    settings = Settings()
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    c = AppContext(settings, make_sessionmaker(engine), Clock(), Engines(), MemoryGateway())  # 운영: 실제 게이트웨이
    with c.sessionmaker() as db:
        if argv[0] == "daily":
            print(len(run_daily(db, c, c.clock.today())), "elders")
        elif argv[0] == "dispatch":
            print(dispatch_due(db, c, c.clock.now()))
        elif argv[0] == "create-admin":
            db.add(m.User(role="admin", phone=argv[1], name=argv[2], created_at=c.clock.now()))
        else:
            raise SystemExit(__doc__)
        db.commit()


if __name__ == "__main__":
    main(sys.argv[1:] or ["--help"])
