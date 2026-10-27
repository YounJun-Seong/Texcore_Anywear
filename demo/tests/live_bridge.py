"""watch_bridge.py --simulate ↔ 단독 HTML 파일 연결 시험.
브리지 연결 → 실시간 심박 표시 → 운동 중 심박 공급 → 브리지 종료 시 안전 엔진이 '심박 끊김'으로 대처하는지.
    LD_LIBRARY_PATH=... ../.venv/bin/python tests/live_bridge.py
"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parents[1]
BRIDGE = HERE.parent / "watch_bridge" / "watch_bridge.py"


def main():
    proc = subprocess.Popen([sys.executable, str(BRIDGE), "serve", "--simulate", "--port", "8765"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(2)
    problems = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1400, "height": 1000})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto((HERE / "dist" / "운동친구_시연.html").resolve().as_uri())
            pg.wait_for_timeout(500)
            pg.click("#liveBtn")
            pg.wait_for_function("document.querySelector('#liveState').innerText.includes('실시간 심박')", timeout=10000)
            if "실시간" not in pg.inner_text("#elder"):
                problems.append("홈 화면에 실시간 워치 카드가 없음")
            if pg.inner_text("#speed .on") != "1배":
                problems.append("실시간 연결 중 배속이 1배가 아님")
            # 운동 시작(초록)
            for sel in ["[data-e=start]"]:
                pg.click(sel)
            pg.fill("#bp_s", "128"); pg.fill("#bp_d", "78"); pg.fill("#bp_p", "72")
            pg.click("[data-e=bpNext]")
            for _ in range(3):
                pg.click("[data-e='ans:']")
            pg.click("[data-e=submit]")
            pg.click("[data-e=go]")
            pg.wait_for_timeout(6000)
            elder = pg.inner_text("#elder")
            if "(실시간)" not in elder:
                problems.append("운동 화면에 실시간 심박 표시 없음")
            log = pg.inner_text("#log")
            if "디즈먼트 워치" not in log:
                problems.append("판정 기록에 심박 출처(디즈먼트 워치) 없음")
            if "심박 끊김" in log:
                problems.append("심박이 오는데도 끊김으로 판단함")
            # 브리지 종료 → 15초 넘게 심박 없음 → 센서 오류 대처
            proc.terminate()
            proc.wait(5)
            pg.wait_for_function("document.querySelector('#log').innerText.includes('심박 끊김')", timeout=30000)
            if "센서 오류 대처" not in pg.inner_text("#log"):
                problems.append("끊김 뒤 센서 오류 대처 기록 없음")
            if len(sys.argv) > 1:
                pg.screenshot(path=str(Path(sys.argv[1]) / "live.png"))
            if errs:
                problems.append(f"페이지 오류: {errs[:3]}")
            b.close()
    finally:
        if proc.poll() is None:
            proc.terminate()
        out = proc.stdout.read() if proc.stdout else ""
    print("브리지 출력:\n" + "\n".join(out.splitlines()[:6]))
    print("문제 없음" if not problems else "\n".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
