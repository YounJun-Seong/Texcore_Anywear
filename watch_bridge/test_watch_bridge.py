import asyncio
import json

import pytest

from watch_bridge import Hub, main, parse_heart_rate


@pytest.mark.parametrize("data,expected", [
    (bytes([0x00, 72]), (72, None)),                      # 8비트, 접촉 감지 없음
    (bytes([0x01, 0x2C, 0x01]), (300, None)),             # 16비트 리틀엔디언
    (bytes([0x06, 95]), (95, True)),                      # 접촉 감지 지원 + 접촉됨
    (bytes([0x04, 95]), (95, False)),                     # 접촉 감지 지원 + 떨어짐
    (bytes([0x10, 80, 0x00, 0x04]), (80, None)),          # RR 간격이 붙어 있어도 심박만
    (bytes([0x19, 0x7E, 0x00, 0x20, 0x01]), (126, None)), # 16비트 + 에너지 + RR
])
def test_parse_heart_rate(data, expected):
    assert parse_heart_rate(data) == expected


@pytest.mark.parametrize("data", [b"", bytes([0x00]), bytes([0x01, 0x10])])
def test_parse_rejects_short_packets(data):
    with pytest.raises(ValueError):
        parse_heart_rate(data)


def test_hub_records_gaps_and_broadcasts(tmp_path, monkeypatch):
    import watch_bridge
    monkeypatch.setattr(watch_bridge, "OUT", tmp_path)

    class FakeWS:
        def __init__(self):
            self.sent = []

        async def send(self, data):
            self.sent.append(json.loads(data))

    async def run():
        hub = Hub("test")
        ws = FakeWS()
        hub.clients.add(ws)
        await hub.send({"type": "status", "state": "connected"})
        await hub.heart_rate(90, True, 70)
        await hub.heart_rate(95, True, 70)
        return hub, ws

    hub, ws = asyncio.run(run())
    assert [m["type"] for m in ws.sent] == ["status", "hr", "hr"]
    assert ws.sent[2]["bpm"] == 95 and ws.sent[2]["source"] == "test"
    rows = hub.csv_path.read_text(encoding="utf-8").splitlines()
    assert rows[0] == "time,bpm,contact,gap_seconds" and len(rows) == 3
    assert rows[1].endswith(",90,True,")                 # 첫 건은 간격 없음


def test_cli_requires_command():
    with pytest.raises(SystemExit):
        main([])
