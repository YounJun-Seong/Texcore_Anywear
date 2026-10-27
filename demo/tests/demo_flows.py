"""시연 페이지를 헤드리스 브라우저에서 돌려 상황 6개가 끝까지 가는지, 화면이 넘치지 않는지 확인하고 스크린샷을 남긴다.
    LD_LIBRARY_PATH=... ../.venv/bin/python tests/demo_flows.py <스크린샷 폴더>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "shots"
OUT.mkdir(parents=True, exist_ok=True)
# 게시 때 씌워지는 문서 뼈대를 흉내 낸다
HTML = ("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        "<style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>"
        "</head><body>" + (HERE / "dist" / "index.html").read_text(encoding="utf-8") + "</body></html>")

EXPECT = {
    "green": ("해내셨어요", ["오늘 운동했어요"], "complete"),
    "yellow": ("5분", [], "session_or_rpe"),
    "red": ("빨강 · 오늘은 쉬어요", [], "result"),
    "hard": ("보호자에게 알렸어요", ["운동 중 몸이 불편하다고 하셨어요"], "emergency"),
    "hr": ("천천히", [], "session"),
    "chest": ("119 전화하기", ["급한 증상을 알려 오셨어요"], "emergency"),
    "strapHigh": ("괜찮으세요?", [], "emergency"),
    "watchHigh": ("워치는 참고용이라 멈추지 않고", [], "session"),
    "watchBp": ("초록 · 평소대로 해요", [], "result"),
}
# 같은 심박이어도 출처 등급에 따라 판정 기록이 달라야 한다
LOG_MUST = {
    "strapHigh": ["가슴 스트랩(A 등급) 심박이라 바로 중단", "HR_FAR_OVER_CEILING"],
    "watchHigh": ["디즈먼트 워치(B 등급) 심박이라 중단하지 않고 일시정지까지만", "HR_FAR_OVER_CEILING"],
    "watchBp": ["PRE_BP_SOURCE_NOT_ALLOWED", "디즈먼트 워치 측정", "다시 재 주세요"],
}


def run():
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for scheme in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1400, "height": 1000}, color_scheme=scheme)
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.set_content(HTML, wait_until="load")
            pg.wait_for_timeout(500)
            if scheme == "light":
                for name, (elder_text, guardian_texts, _) in EXPECT.items():
                    pg.click(f"[data-scn={name}]")
                    try:
                        pg.wait_for_function(f"document.querySelector('#elder').innerText.includes({elder_text!r})", timeout=30000)
                    except Exception:
                        problems.append(f"{name}: 어르신 화면에 '{elder_text}' 안 나옴 → {pg.inner_text('#elder')[:200]!r}")
                        continue
                    pg.wait_for_timeout(1500)
                    g = pg.inner_text("#guardian")
                    for t in guardian_texts:
                        if t not in g:
                            problems.append(f"{name}: 보호자 화면에 '{t}' 없음")
                    log = pg.inner_text("#log")
                    if "판정" not in log and name != "chest":
                        problems.append(f"{name}: 판정 기록 비어 있음")
                    for must in LOG_MUST.get(name, []):
                        if must not in log:
                            problems.append(f"{name}: 판정 기록에 '{must}' 없음")
                    if name == "watchHigh" and "중단" in pg.inner_text("#elder").split("\n")[0:3]:
                        problems.append("watchHigh: 워치인데 중단됨")
                    pg.screenshot(path=str(OUT / f"scn_{name}.png"), full_page=False)
                # 공유 범위 "응원만"이면 "오늘 운동했어요"가 가지 않아야 한다
                pg.click("[data-scope=cheer_only]")
                pg.click("[data-scn=green]")
                pg.wait_for_function("document.querySelector('#elder').innerText.includes('해내셨어요')", timeout=30000)
                if "오늘 운동했어요" in pg.inner_text("#guardian"):
                    problems.append("응원만 범위인데 운동 여부가 보호자에게 감")
                pg.click("[data-scope=full]")
            else:
                pg.click("[data-scn=hard]")
                pg.wait_for_function("document.querySelector('#elder').innerText.includes('보호자에게 알렸어요')", timeout=30000)
                pg.wait_for_timeout(800)
            pg.screenshot(path=str(OUT / f"desktop_{scheme}.png"), full_page=True)
            overflow = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if overflow:
                problems.append(f"{scheme}: 가로 스크롤 생김")
            if errs:
                problems.append(f"{scheme}: 콘솔 오류 {errs[:3]}")
            pg.close()

        # 휴대폰 폭
        pg = b.new_page(viewport={"width": 400, "height": 860}, color_scheme="light")
        pg.set_content(HTML, wait_until="load")
        pg.click("[data-scn=yellow]")
        pg.wait_for_function("document.querySelector('#elder').innerText.includes('5분')", timeout=30000)
        pg.wait_for_timeout(1200)
        pg.screenshot(path=str(OUT / "phone.png"), full_page=False)
        if pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"):
            problems.append("휴대폰 폭에서 가로 스크롤 생김")
        b.close()
    print("문제 없음" if not problems else "\n".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(run())
