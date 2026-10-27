"""시연 페이지 조립: page.html + 컴파일된 안전 엔진(engine.js) + 규칙 번들 → dist/index.html (파일 하나).

    cd ../safety_dart && dart compile js -O2 -o ../demo/engine.js web/bridge.dart
    python build.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "safety"))
from safety_engine import load_rules  # noqa: E402


def main():
    page = (HERE / "src" / "page.html").read_text(encoding="utf-8")
    engine = (HERE / "engine.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    bundle = json.dumps(load_rules().data, ensure_ascii=False, separators=(",", ":"))
    assert "/*__ENGINE__*/" in page and "/*__BUNDLE__*/" in page
    out = page.replace("/*__ENGINE__*/", engine).replace("/*__BUNDLE__*/", bundle)
    (HERE / "dist").mkdir(exist_ok=True)
    (HERE / "dist" / "index.html").write_text(out, encoding="utf-8")
    # 게시 없이 더블클릭으로 여는 단독 파일(문서 뼈대 포함). 인터넷이 없으면 글꼴만 기본 글꼴로 바뀐다.
    standalone = ("<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
                  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                  "<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n" + out + "\n</body>\n</html>\n")
    (HERE / "dist" / "운동친구_시연.html").write_text(standalone, encoding="utf-8")
    print(f"dist/index.html, dist/운동친구_시연.html {len(standalone.encode()) // 1024}KB")


if __name__ == "__main__":
    main()
