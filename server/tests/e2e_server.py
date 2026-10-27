"""단말 앱 계약 테스트용 서버 실행기(운영 코드 아님).

보낸 문자를 파일에 적는 게이트웨이를 끼워, 앱 테스트가 인증번호를 읽을 수 있게 한다.
서버 인증 코드에는 테스트용 우회 경로를 두지 않는다.

    SMS_FILE=/tmp/sms.txt python tests/e2e_server.py 8766
"""
import os
import sys
from pathlib import Path

import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import Settings  # noqa: E402
from app.gateway import MemoryGateway  # noqa: E402
from app.main import create_app  # noqa: E402


class FileSmsGateway(MemoryGateway):
    def send(self, msg):
        super().send(msg)
        if msg.channel == "sms":
            with open(os.environ["SMS_FILE"], "a", encoding="utf-8") as f:
                f.write(f"{msg.to_phone} {msg.data['code']}\n")


if __name__ == "__main__":
    app = create_app(Settings(database_url="sqlite://", allow_draft_rules=True), gateway=FileSmsGateway())
    uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[1]), log_level="warning")
