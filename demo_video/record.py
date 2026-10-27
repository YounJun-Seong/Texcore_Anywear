"""운동친구 실제 앱 시연 영상 녹화.

실제 Flutter 앱(웹 빌드, 휴대폰 크기) + 실제 서버 + 실제 워치 브리지(가상 워치)를 띄우고,
사람이 누르듯 앱을 조작하며 녹화한다. 기다리는 구간은 표시해 두었다가 mp4로 바꿀 때 빠르게 돌린다.

    LD_LIBRARY_PATH=... ../.venv/bin/python record.py out.mp4
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PY = sys.executable
ELDER, GUARDIAN = "01011112222", "01033334444"
PACE = 0.9
FAST = 5            # 기다리는 구간 배속


def api(method, path, body=None, token=None):
    req = urllib.request.Request(f"http://localhost:8000{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"content-type": "application/json", **({"authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read() or b"null")


def otp(phone):
    return api("GET", f"/__demo/otp?phone={phone}")["code"]


def start_bridge(phase):
    return subprocess.Popen([PY, str(ROOT / "watch_bridge" / "watch_bridge.py"), "serve", "--simulate", "--start-phase", str(phase)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main(out_mp4):
    server = subprocess.Popen([PY, str(HERE / "stage_server.py")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    bridge = start_bridge(0)
    for _ in range(60):                 # 서버가 실제로 응답할 때까지 기다림
        try:
            api("GET", "/health")
            break
        except Exception:
            time.sleep(0.5)
    time.sleep(1)
    marks = []          # (초, 'fast'|'normal')
    video_dir = HERE / "raw"
    video_dir.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, record_video_dir=str(video_dir),
                                record_video_size={"width": 1440, "height": 900})
            page = ctx.new_page()
            t0 = time.time()
            page.goto("http://localhost:8000/stage")
            F = page.frame_locator("#app")

            def cap(n, title, desc=""):
                page.evaluate("([n,t,d]) => window.caption(n,t,d)", [n, title, desc])

            def fast(on):
                marks.append((time.time() - t0, "fast" if on else "normal"))
                page.evaluate("on => window.setFast && window.setFast(on)", on)

            def btn(text):
                return F.locator('flt-semantics[role="button"]').filter(has_text=text).last

            def tap(text, wait=PACE):
                loc = btn(text)
                loc.wait_for(timeout=60000)
                loc.click()
                time.sleep(wait)

            def typ(label, value):
                f = F.locator(f'input[aria-label="{label}"]').last
                f.wait_for(timeout=30000)
                f.click()
                page.keyboard.type(value, delay=110)
                time.sleep(0.4)

            def see(text, timeout=60000):
                F.get_by_text(text).last.wait_for(timeout=timeout)

            time.sleep(6)                                   # 앱 첫 로딩
            # 1. 가입
            cap(1, "휴대폰 번호로 시작", "아이디·비밀번호 없이 휴대폰 번호와 문자 인증번호로 시작합니다. 보호자나 복지사가 대신 설정할 수도 있어요.")
            time.sleep(2.5)
            typ("휴대폰 번호", ELDER)
            tap("인증번호 받기")
            typ("문자로 온 인증번호", otp(ELDER))
            tap("확인", 1.5)
            cap(2, "기본 정보와 건강 정보 동의", "이름·태어난 해를 넣고, 건강 정보는 항목을 보여 드린 뒤 따로 동의를 받습니다.")
            typ("이름", "김영자")
            tap("다음")
            typ("예: 1952", "1952")
            tap("다음", 1.5)
            time.sleep(2)
            tap("동의해요", 1.2)
            cap(3, "질환 확인과 운동 전 문진", "의사 확인이 필요한 심장 질환, 맥박을 느리게 하는 약, 심장 박동기를 묻고, 몸 상태 질문 7개에 답합니다.")
            time.sleep(1.5)
            tap("해당 없어요")
            tap("안 먹어요")
            tap("아니요")
            tap("다음", 1.2)
            for _ in range(7):
                tap("아니요", 0.7)
            see("혈압 재고 시작하기")
            time.sleep(1.5)

            # 2. 보호자 연결 (딸이 보호자 앱에서 요청 → 어르신이 수락하고 공유 범위 선택)
            api("POST", "/auth/otp/request", {"phone": GUARDIAN})
            gtok = api("POST", "/auth/otp/verify", {"phone": GUARDIAN, "code": otp(GUARDIAN), "role": "guardian", "name": "이지은"})["token"]
            api("POST", "/guardian/links", {"elder_phone": ELDER}, gtok)
            cap(4, "보호자 연결: 어르신이 직접 고릅니다", "딸이 연결을 요청했어요. 무엇을 알릴지는 어르신이 고르고, 언제든 바꾸거나 끊을 수 있습니다.")
            tap("보호자 연결", 1.5)
            tap("연결하기", 1.5)
            tap("오늘 운동했는지와 주간 요약도 알려요", 2)
            F.locator('flt-semantics[role="button"]').filter(has_text="뒤로").last.click()
            time.sleep(1.5)

            # 3. 워치 연결
            bridge.terminate(); bridge.wait(5)
            bridge = start_bridge(70)                       # 운동 시작 후 약 25초 뒤에 심박 126 구간
            time.sleep(1.5)
            cap(5, "디즈먼트 워치 연결", "워치 → PC 파이썬 브리지 → 앱. 앱 안의 안전 엔진이 워치 심박을 B 등급(경고용)으로 판정합니다.")
            tap("워치 연결하기", 2.5)
            see("심박")
            time.sleep(1.5)

            # 4. 운동 전 점검
            cap(6, "운동 전 점검: 혈압과 몸 상태", "팔에 감는 혈압계 숫자와 짧은 질문 세 개. 판정은 휴대폰 안에서 하고, 서버도 같은 판정을 다시 합니다.")
            tap("혈압 재고 시작하기", 1.2)
            typ("높은 쪽 숫자(수축기)", "130")
            typ("낮은 쪽 숫자(이완기)", "80")
            typ("맥박", "70")
            tap("다음")
            tap("아니요, 괜찮아요")
            tap("아니요")
            tap("아니요")
            tap("결과 보기", 2.5)
            cap(7, "초록: 평소대로 3분", "수축기·이완기·맥박 모두 정상 → 오늘 단계(3분) 그대로. 더 쉬운 걸로(1분)도 고를 수 있어요.")
            time.sleep(3.5)

            # 5. 운동 + 워치
            tap("3분 시작하기", 2)
            cap(8, "운동 중: 워치 심박을 실시간으로", "디즈먼트 워치 (실시간) 카드에 심박이 매초 들어옵니다. 오늘 심박 상한은 109회/분입니다.")
            time.sleep(6)
            fast(True)
            see("잠깐 쉬는 중", timeout=150000)
            fast(False)
            cap(9, "심박 126: 워치는 일시정지까지만", "상한의 +10%를 넘었지만 워치 값은 참고용(B 등급)이라 중단하지 않고 쉬게 합니다. 가슴 스트랩(A 등급)이었다면 바로 중단합니다.")
            time.sleep(7)
            fast(True)
            # 쉬는 동안 심박이 내려오면(12초 넘게 105 아래) 다시 하기
            calm = 0
            while calm < 12:
                bpm = page.evaluate("window.lastBpm")
                calm = calm + 1 if bpm is not None and bpm < 105 else 0
                time.sleep(1)
            fast(False)
            cap(10, "쉬고 나서 다시 하기", "심박이 내려온 뒤 다시 시작합니다.")
            tap("다시 하기", 3)
            fast(True)
            see("워치 신호가 끊겼어요", timeout=180000)
            fast(False)
            cap(11, "워치 신호가 끊기면", "없는 값을 채우지 않습니다. 강도를 낮추고 숨찬 정도를 더 자주 여쭤봅니다.")
            time.sleep(4)
            fast(True)
            try:
                btn("편해요, 말도 잘 나와요").wait_for(timeout=90000)
                fast(False)
                cap(12, "숨찬 정도 질문", "심박이 없을 때는 1분마다 묻습니다. 말할 수 있을 정도면 알맞은 강도예요.")
                time.sleep(2.5)
                tap("편해요, 말도 잘 나와요", 2)
                fast(True)
            except Exception:
                pass
            while True:      # 남은 운동 중 다시 묻는 질문에도 답하며 완료까지
                if F.get_by_text("해내셨어요").count():
                    break
                q = btn("편해요, 말도 잘 나와요")
                if q.count():
                    q.click()
                time.sleep(1)
            fast(False)
            cap(13, "완료: 칭찬과 도장, 보호자에게 한 줄", "도장은 운동량이 아니라 '시작한 것'에 줍니다. 공유 범위가 '모두'인 딸에게만 '오늘 운동했어요'가 갑니다.")
            time.sleep(7)
            tap("확인", 2)

            # 6. 응급: 가슴 통증
            cap(14, "가슴 통증을 알리면", "판정을 기다리지 않고 바로 119 안내로 넘어가고, 공유 범위와 관계없이 보호자에게 전화와 알림이 갑니다.")
            tap("혈압 재고 시작하기", 1.2)
            typ("높은 쪽 숫자(수축기)", "142")
            typ("낮은 쪽 숫자(이완기)", "88")
            typ("맥박", "96")
            tap("다음")
            tap("가슴이 아프거나 조여요", 3)
            tap("도움 요청하기", 3)
            see("119 전화하기")
            time.sleep(6)
            cap(15, "운동친구", "판정은 규칙으로, 말투만 부드럽게. 실제 워치가 오면 브리지만 실제 주소로 바꾸면 됩니다.")
            time.sleep(5)
            video_path = page.video.path()
            total = time.time() - t0
            ctx.close()
            b.close()
    finally:
        bridge.terminate()
        server.terminate()
    encode(Path(video_path), marks, total, Path(out_mp4))


def encode(src, marks, total, out):
    """기다리는 구간(fast)만 FAST배로 빠르게 해서 mp4로."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    segs, cur, start = [], "normal", 0.0
    for t, kind in marks:
        if t > start:
            segs.append((start, t, cur))
        start, cur = t, kind
    segs.append((start, total, cur))
    parts = []
    for i, (a, b, kind) in enumerate(segs):
        speed = FAST if kind == "fast" else 1
        parts.append(f"[0:v]trim=start={a:.2f}:end={b:.2f},setpts=(PTS-STARTPTS)/{speed}[v{i}]")
    graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,fps=30[out]"
    subprocess.run([ff, "-y", "-i", str(src), "-filter_complex", graph, "-map", "[out]", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium", "-movflags", "+faststart", str(out)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{out} 저장 (원본 {total:.0f}초, 빠르게 구간 {sum(b - a for a, b, k in segs if k == 'fast'):.0f}초)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "운동친구_시연영상.mp4"))
