"""시연 영상 녹화용 무대(운영 코드 아님).

한 주소(http://localhost:8000)에서 실제 서버 API + Flutter 앱(/app/) + 자막 화면(/stage)을 함께 연다.
같은 주소라 브라우저 보안(CORS) 문제 없이 앱이 실제 서버와 통신한다.
인증번호는 문자 대신 /__demo/otp 로 녹화 스크립트에 넘긴다(이 실행기에만 있음).
"""
import sys
from pathlib import Path

import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
from app.config import Settings  # noqa: E402
from app.gateway import MemoryGateway  # noqa: E402
from app.main import create_app  # noqa: E402

gateway = MemoryGateway()
app = create_app(Settings(database_url="sqlite://", allow_draft_rules=True), gateway=gateway)


@app.get("/__demo/otp")
def last_otp(phone: str):
    codes = [m.data["code"] for m in gateway.sent if m.channel == "sms" and m.to_phone == phone]
    return {"code": codes[-1] if codes else None}


@app.get("/__demo/outbox")
def outbox():
    return [{"channel": m.channel, "to": m.to_user_id, "title": m.title, "body": m.body} for m in gateway.sent if m.channel != "sms"]


@app.get("/stage")
def stage():
    return FileResponse(Path(__file__).with_name("stage.html"))


app.mount("/app", StaticFiles(directory=ROOT / "mobile" / "build" / "web", html=True), name="app")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
