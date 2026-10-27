"""단말용 안전 규칙 번들 배포. 단말은 이 번들로 오프라인 판정하고, 버전·해시를 판정 로그에 남긴다.
자문단 승인(approved) 번들만 내려보낸다. 개발 중에는 ALLOW_DRAFT_RULES=1."""
import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from ..deps import AppContext, ctx

router = APIRouter(prefix="/rules", tags=["rules"])


def _bundle(c: AppContext):
    rules = c.engines.safety_rules
    if not rules.approved and not c.settings.allow_draft_rules:
        raise HTTPException(503, f"승인된 안전 규칙이 없어요 (현재 {rules.version}, draft)")
    return rules


@router.get("/safety/version")
def version(c: AppContext = Depends(ctx)):
    rules = c.engines.safety_rules
    return {"version": rules.version, "sha256": rules.sha256, "status": rules["meta"]["status"]}


@router.get("/safety")
def bundle(request: Request, c: AppContext = Depends(ctx)):
    rules = _bundle(c)
    etag = f'"{rules.sha256}"'
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers={"ETag": etag})
    body = '{"version":%s,"sha256":"%s","rules":%s}' % (json.dumps(rules.version), rules.sha256, rules.to_json())
    return Response(content=body, media_type="application/json", headers={"ETag": etag})
