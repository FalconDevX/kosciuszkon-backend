"""Parse POST /ai/chat body: JSON (AIChatRequest) or multipart like rag_api."""

from __future__ import annotations

import json

from fastapi import HTTPException, Request
from starlette.datastructures import UploadFile

async def parse_ai_chat_request(request: Request) -> tuple[
    str,
    list[dict[str, str]],
    tuple[bytes, str] | None,
    str | None,
    str | None,
]:
    """
    Returns: message, history, upload_bytes_pair_or_none, file_base64_or_none, file_name_or_none.
    """
    ct = (request.headers.get("content-type") or "").lower()

    if "multipart/form-data" in ct:
        form = await request.form()
        msg_val = form.get("message")
        if msg_val is None or not str(msg_val).strip():
            raise HTTPException(status_code=422, detail="message is required")
        message = str(msg_val).strip()

        hist_val = form.get("history")
        hist_raw = hist_val if isinstance(hist_val, str) else "[]"
        try:
            history_payload = json.loads(hist_raw or "[]")
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=422, detail=f"invalid history JSON: {exc}") from exc

        history = _normalize_history(history_payload)
        uploaded: tuple[bytes, str] | None = None
        up = form.get("file")
        if up is not None:
            if not isinstance(up, UploadFile):
                raise HTTPException(status_code=422, detail="file must be an upload")
            raw_bytes = await up.read()
            if raw_bytes:
                fname = up.filename or "upload.bin"
                uploaded = (raw_bytes, fname)
        return message, history, uploaded, None, None

    try:
        body = await request.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="invalid JSON body") from exc

    from app.schemas.ai import AIChatRequest

    try:
        parsed = AIChatRequest.model_validate(body)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    message = parsed.message.strip()
    history = _normalize_history(parsed.history)
    fb64 = parsed.file_base64.strip() if parsed.file_base64 else None
    fname = (parsed.file_name or "").strip() or None
    return message, history, None, fb64, fname


def _normalize_history(raw: object) -> list[dict[str, str]]:
    if not isinstance(raw, list):
        return []
    out: list[dict[str, str]] = []
    for h in raw[-16:]:
        if not isinstance(h, dict):
            continue
        role = h.get("role")
        content = h.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            out.append({"role": role, "content": content.strip()})
    return out
