"""바깥으로 나가는 연결(푸시·전화·문자). 운영에서는 FCM·국내 문자/음성 사업자 구현으로 바꾼다.

위치 정보는 여기서 응급 알림에 실어 보내기만 하고 DB에는 남기지 않는다.
"""
from dataclasses import dataclass, field


@dataclass
class Outbound:
    channel: str          # push | call | sms
    to_user_id: int | None
    to_phone: str | None
    title: str
    body: str
    data: dict = field(default_factory=dict)


class Gateway:
    def send(self, msg: Outbound) -> None:
        raise NotImplementedError


class MemoryGateway(Gateway):
    """개발·테스트용: 보낸 것을 메모리에 쌓는다."""

    def __init__(self):
        self.sent: list[Outbound] = []

    def send(self, msg):
        self.sent.append(msg)
