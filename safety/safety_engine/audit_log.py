"""변경 불가 판정 로그(5-5): 입력 → 판정 → 사유 코드 + 규칙 버전.

추가 전용 JSONL에 해시 체인을 건다. 한 줄이라도 고치거나 지우면 verify()가 위치를 찾아낸다.
서버에서는 같은 레코드를 추가 전용 테이블에 저장한다(이 모듈은 단말·테스트용 기준 구현).
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0" * 64


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def record_hash(record):
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()


class DecisionLog:
    def __init__(self, path):
        self.path = Path(path)
        self.seq, self.prev = 0, GENESIS
        if self.path.exists():
            for rec in self._read():
                self.seq, self.prev = rec["seq"] + 1, rec["hash"]

    def _read(self):
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)

    def append(self, kind, payload, rule_version, rule_sha256, ts=None):
        rec = {
            "seq": self.seq,
            "ts": ts or datetime.now(timezone.utc).isoformat(),
            "kind": kind,
            "rule_version": rule_version,
            "rule_sha256": rule_sha256,
            "payload": payload,
            "prev_hash": self.prev,
        }
        rec["hash"] = record_hash(rec)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(canonical(rec) + "\n")
        self.seq, self.prev = self.seq + 1, rec["hash"]
        return rec

    def verify(self):
        """(정상 여부, 처음 깨진 seq 또는 None)"""
        prev, expected_seq = GENESIS, 0
        for rec in self._read():
            if rec["seq"] != expected_seq or rec["prev_hash"] != prev or rec["hash"] != record_hash(rec):
                return False, expected_seq
            prev, expected_seq = rec["hash"], expected_seq + 1
        return True, None
