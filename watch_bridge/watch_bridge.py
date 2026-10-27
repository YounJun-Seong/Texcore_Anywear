"""디즈먼트 워치(Diz-SW01) ↔ 시연 HTML 연결 다리.

내 컴퓨터의 블루투스로 워치에 붙어 심박을 받고, 같은 컴퓨터에서 연 시연 HTML에 WebSocket으로 넘긴다.

    python watch_bridge.py scan                      # 주변 블루투스 기기 찾기
    python watch_bridge.py inspect <주소>             # 워치가 공개하는 서비스 목록 + 표준 심박 서비스 여부 (PoC-0 기록 저장)
    python watch_bridge.py serve --address <주소>     # 심박을 받아 ws://localhost:8765 로 중계
    python watch_bridge.py serve --simulate          # 워치 없이 가짜 심박으로 HTML 연결 시험

원칙(계획서 7-3)
- 표준 블루투스 심박 서비스(Heart Rate Service, 0x180D)만 쓴다. 워치가 이것을 공개하지 않으면 여기서 멈춘다.
  제조사 허락 없이 비공개 통신 규격을 분석하지 않는다. 그때는 헬스 앱 경유 / 공급사 협력 / 폰만으로 중 하나로 간다.
- 워치 심박은 B 등급(경고용)이다. 판정은 HTML 안의 안전 엔진이 등급 규칙대로 한다(중단 대신 일시정지까지만).
- 대부분 워치는 한 번에 한 기기에만 연결된다. 연결 전에 휴대폰의 워치 앱 연결을 끊거나 휴대폰 블루투스를 꺼 둔다.
"""
import argparse
import asyncio
import csv
import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path

HR_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HR_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"
KNOWN = {
    "0000180d": "심박(Heart Rate) — 표준",
    "0000180f": "배터리(Battery) — 표준",
    "0000180a": "기기 정보(Device Information) — 표준",
    "00001800": "일반 접근(Generic Access) — 표준",
    "00001801": "일반 속성(Generic Attribute) — 표준",
}
NAME_HINTS = ("diz", "sw01", "smart", "watch", "q3", "r4", "r5")
OUT = Path(__file__).resolve().parent / "records"


def parse_heart_rate(data: bytes):
    """표준 Heart Rate Measurement(0x2A37) 해석. 반환: (심박 bpm, 피부 접촉 여부 또는 None)."""
    if not data:
        raise ValueError("empty heart rate packet")
    flags = data[0]
    if flags & 0x01:            # 심박이 16비트
        if len(data) < 3:
            raise ValueError("short 16-bit heart rate packet")
        bpm = int.from_bytes(data[1:3], "little")
    else:                       # 8비트
        if len(data) < 2:
            raise ValueError("short 8-bit heart rate packet")
        bpm = data[1]
    contact = None
    if flags & 0x04:            # 접촉 감지 지원
        contact = bool(flags & 0x02)
    return bpm, contact


def stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------- scan / inspect ----------------
async def scan(seconds):
    from bleak import BleakScanner
    print(f"{seconds}초 동안 주변 블루투스 기기를 찾습니다… (워치 화면을 켜 두세요)")
    found = await BleakScanner.discover(timeout=seconds, return_adv=True)
    rows = sorted(found.values(), key=lambda x: -(x[1].rssi or -999))
    for dev, adv in rows:
        name = dev.name or adv.local_name or "(이름 없음)"
        hint = "  ← 워치일 수 있음" if any(h in name.lower() for h in NAME_HINTS) else ""
        hr = "  [표준 심박 서비스 광고]" if HR_SERVICE in [u.lower() for u in adv.service_uuids] else ""
        print(f"{dev.address}  신호 {adv.rssi:>4}  {name}{hint}{hr}")
    if not rows:
        print("찾은 기기가 없습니다. 블루투스가 켜져 있는지, 워치가 휴대폰과 연결되어 있지 않은지 확인하세요.")


async def inspect(address):
    from bleak import BleakClient
    OUT.mkdir(exist_ok=True)
    report = {"address": address, "checked_at": datetime.now().isoformat(), "services": [], "has_heart_rate_service": False}
    print(f"{address} 에 연결합니다…")
    async with BleakClient(address, timeout=20) as client:
        for svc in client.services:
            label = KNOWN.get(svc.uuid[:8], "제조사 전용(비공개)")
            chars = [{"uuid": c.uuid, "properties": c.properties} for c in svc.characteristics]
            report["services"].append({"uuid": svc.uuid, "label": label, "characteristics": chars})
            print(f"- {svc.uuid}  {label}")
            for c in chars:
                print(f"    · {c['uuid']}  {', '.join(c['properties'])}")
        report["has_heart_rate_service"] = any(s["uuid"].lower() == HR_SERVICE for s in report["services"])
        try:
            report["battery"] = (await client.read_gatt_char(BATTERY_LEVEL))[0]
        except Exception:
            report["battery"] = None
    path = OUT / f"inspect_{stamp()}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    if report["has_heart_rate_service"]:
        print("✓ 표준 심박 서비스가 있습니다. 'serve --address' 로 HTML에 연결할 수 있어요.")
    else:
        print("✗ 표준 심박 서비스가 없습니다. 이 워치는 블루투스 직접 연결(B안)로는 심박을 받을 수 없어요.")
        print("  다음 단계(계획서 7-3): 헬스 앱 경유(A안) 또는 공급사 협력(C안). 비공개 규격은 허락 없이 분석하지 않습니다.")
    print(f"기록 저장: {path}")


# ---------------- serve ----------------
class Hub:
    """브라우저 연결들에 메시지를 뿌리고, 받은 심박을 CSV로 남긴다(전송 간격·끊김 = PoC-0 기록)."""

    def __init__(self, source):
        self.clients = set()
        self.source = source
        self.last = {"type": "status", "state": "starting", "source": source}
        OUT.mkdir(exist_ok=True)
        self.csv_path = OUT / f"hr_{source}_{stamp()}.csv"
        self._f = open(self.csv_path, "w", newline="", encoding="utf-8")
        self._w = csv.writer(self._f)
        self._w.writerow(["time", "bpm", "contact", "gap_seconds"])
        self._prev = None
        self.count = 0

    async def send(self, msg):
        if msg["type"] == "status":
            self.last = msg
            print(f"[상태] {msg['state']}" + (f" — {msg['detail']}" if msg.get("detail") else ""))
        data = json.dumps(msg, ensure_ascii=False)
        for ws in list(self.clients):
            try:
                await ws.send(data)
            except Exception:
                self.clients.discard(ws)

    async def heart_rate(self, bpm, contact=None, battery=None):
        now = time.time()
        gap = None if self._prev is None else round(now - self._prev, 2)
        self._prev = now
        self.count += 1
        self._w.writerow([datetime.now().isoformat(timespec="seconds"), bpm, contact, gap])
        self._f.flush()
        if self.count % 10 == 1:
            print(f"[심박] {bpm} bpm (간격 {gap}s, 누적 {self.count}건)")
        await self.send({"type": "hr", "bpm": bpm, "contact": contact, "battery": battery, "ts": now, "source": self.source})

    async def handler(self, ws):
        self.clients.add(ws)
        await ws.send(json.dumps(self.last, ensure_ascii=False))
        try:
            async for _ in ws:
                pass
        finally:
            self.clients.discard(ws)


async def run_watch(hub: Hub, address, name):
    from bleak import BleakClient, BleakScanner
    while True:
        try:
            target = address
            if not target:
                await hub.send({"type": "status", "state": "scanning", "detail": f"이름에 '{name}' 포함된 기기 찾는 중"})
                dev = await BleakScanner.find_device_by_filter(lambda d, a: name.lower() in (d.name or a.local_name or "").lower(), timeout=15)
                if dev is None:
                    await hub.send({"type": "status", "state": "not_found", "detail": "워치를 찾지 못했어요. 5초 뒤 다시 찾습니다"})
                    await asyncio.sleep(5)
                    continue
                target = dev.address
            await hub.send({"type": "status", "state": "connecting", "detail": target})
            disconnected = asyncio.Event()
            async with BleakClient(target, timeout=20, disconnected_callback=lambda _c: disconnected.set()) as client:
                if not any(s.uuid.lower() == HR_SERVICE for s in client.services):
                    await hub.send({"type": "status", "state": "no_heart_rate_service",
                                    "detail": "표준 심박 서비스가 없어 블루투스로 심박을 받을 수 없어요(계획서 7-3 B안 불가)"})
                    return
                battery = None
                try:
                    battery = (await client.read_gatt_char(BATTERY_LEVEL))[0]
                except Exception:
                    pass

                def on_hr(_char, data: bytearray):
                    try:
                        bpm, contact = parse_heart_rate(bytes(data))
                    except ValueError:
                        return
                    asyncio.get_running_loop().create_task(hub.heart_rate(bpm, contact, battery))

                await client.start_notify(HR_MEASUREMENT, on_hr)
                await hub.send({"type": "status", "state": "connected", "detail": target, "battery": battery})
                await disconnected.wait()
            await hub.send({"type": "status", "state": "disconnected", "detail": "연결이 끊겼어요. 다시 연결합니다"})
        except Exception as e:  # 연결 실패·도중 끊김: 안전 엔진은 심박이 끊긴 것으로 보고 질문을 늘린다
            await hub.send({"type": "status", "state": "error", "detail": str(e)[:200]})
        await asyncio.sleep(3)


async def run_simulator(hub: Hub, interval, start_phase=0):
    """워치 없이 시험: 안정 → 운동 중 상승 → 상한 크게 넘김 → 회복 → 잠깐 끊김."""
    await hub.send({"type": "status", "state": "connected", "detail": "가상 워치(시험용)", "battery": 80})
    t = start_phase
    while True:
        phase = t % 240
        if phase < 40:
            bpm = 90 + 3 * math.sin(t / 5)
        elif phase < 120:
            bpm = 100 + (phase - 40) * 0.12 + 3 * math.sin(t / 4)
        elif phase < 150:
            bpm = 126 + 2 * math.sin(t / 3)
        elif phase < 210:
            bpm = 98 + 3 * math.sin(t / 5)
        else:
            bpm = None          # 30초 끊김(센서 오류 흉내)
        if bpm is not None:
            await hub.heart_rate(round(bpm), True, 80)
        await asyncio.sleep(interval)
        t += interval


def browser_visit(connection, request):
    """브라우저 주소창으로 열면 오류 대신 안내 문장을 보여 준다(이 주소는 앱이 쓰는 통로)."""
    from http import HTTPStatus
    if request.headers.get("Upgrade", "").lower() != "websocket":
        return connection.respond(HTTPStatus.OK, "운동친구 워치 브리지가 켜져 있어요.\n"
                                  "이 주소는 앱이 심박을 받아 가는 통로라 브라우저로는 볼 수 없어요.\n"
                                  "앱은 http://localhost:8000/app/ , HTML 시연은 http://localhost:8000/demo 로 여세요.\n")
    return None


async def serve(args):
    from websockets.asyncio.server import serve as ws_serve
    hub = Hub("simulator" if args.simulate else "diz-sw01")
    async with ws_serve(hub.handler, "localhost", args.port, process_request=browser_visit):
        print(f"HTML 연결 주소: ws://localhost:{args.port}  (시연 HTML의 '내 컴퓨터 워치 연결' 버튼)")
        print(f"심박 기록 파일: {hub.csv_path}")
        if args.simulate:
            await run_simulator(hub, args.interval, args.start_phase)
        else:
            await run_watch(hub, args.address, args.name)
            await asyncio.Future()   # 심박 서비스가 없을 때도 HTML에 상태를 보여 주도록 열어 둔다


def main(argv=None):
    ap = argparse.ArgumentParser(description="디즈먼트 워치 ↔ 시연 HTML 연결")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="주변 블루투스 기기 찾기")
    s.add_argument("--seconds", type=float, default=10)
    i = sub.add_parser("inspect", help="워치가 공개하는 서비스 목록 확인")
    i.add_argument("address")
    v = sub.add_parser("serve", help="심박을 HTML로 중계")
    v.add_argument("--address", help="워치 주소(scan 결과). 없으면 --name 으로 찾음")
    v.add_argument("--name", default="diz", help="주소 대신 이름 일부로 찾기")
    v.add_argument("--port", type=int, default=8765)
    v.add_argument("--simulate", action="store_true", help="워치 없이 가짜 심박으로 시험")
    v.add_argument("--interval", type=float, default=1.0, help="가상 워치 전송 간격(초)")
    v.add_argument("--start-phase", type=float, default=0, help="가상 워치 4분 주기 중 시작 위치(초). 120이면 바로 126 구간")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "scan":
            asyncio.run(scan(args.seconds))
        elif args.cmd == "inspect":
            asyncio.run(inspect(args.address))
        else:
            asyncio.run(serve(args))
    except KeyboardInterrupt:
        print("\n끝냈습니다.")
    except ModuleNotFoundError as e:
        sys.exit(f"필요한 패키지가 없습니다: {e.name}. 먼저 'pip install -r requirements.txt' 를 실행하세요.")


if __name__ == "__main__":
    main()
