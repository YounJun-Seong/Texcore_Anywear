import os
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


@dataclass
class Settings:
    # 운영: 국내 리전 PostgreSQL (예: postgresql+psycopg://...). 테스트·개발: SQLite
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./dev.db"))
    # 자문단 승인 전 draft 규칙을 내려보낼지. 운영에서는 반드시 False.
    allow_draft_rules: bool = field(default_factory=lambda: os.getenv("ALLOW_DRAFT_RULES", "0") == "1")
    token_ttl_days: int = 90
    otp_ttl_seconds: int = 180
    otp_max_attempts: int = 5


class Clock:
    """테스트에서 바꿔 끼울 수 있는 시계. 날짜 계산은 모두 한국 시간 기준."""

    def now(self) -> datetime:
        return datetime.now(KST)

    def today(self):
        return self.now().date()


class FixedClock(Clock):
    def __init__(self, now: datetime):
        self.current = now if now.tzinfo else now.replace(tzinfo=KST)

    def now(self):
        return self.current

    def set(self, now: datetime):
        self.current = now if now.tzinfo else now.replace(tzinfo=KST)
