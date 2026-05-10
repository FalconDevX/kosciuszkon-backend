import json

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.schemas.ai import AIChatResponse, AISource


def _extract_ollama_text(payload: dict) -> str:
    message = payload.get("message", {}) or {}
    return (
        message.get("content")
        or message.get("reasoning_content")
        or payload.get("response")
        or payload.get("output_text")
        or ""
    )


def _normalize_sources(raw: object) -> list[AISource]:
    if not isinstance(raw, list):
        return []
    out: list[AISource] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url") or item.get("href") or "").strip()
        title = str(item.get("title") or "").strip() or url
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(AISource(title=title, url=url))
    return out


async def chat_with_model(
    message: str,
    history: list[dict[str, str]],
    uploaded_file: tuple[bytes, str] | None,
    file_base64: str | None,
    file_name: str | None,
    web_search: bool = False,
) -> AIChatResponse:
    rag_base = (settings.RAG_SERVICE_URL or "").strip().rstrip("/")
    if rag_base:
        try:
            async with httpx.AsyncClient(timeout=settings.RAG_TIMEOUT_SECS) as client:
                if uploaded_file is not None:
                    raw, fname = uploaded_file
                    response = await client.post(
                        f"{rag_base}/chat",
                        data={
                            "message": message,
                            "history": json.dumps(history),
                            "web_search": "true" if web_search else "false",
                        },
                        files={"file": (fname, raw)},
                    )
                else:
                    payload: dict = {
                        "message": message,
                        "history": history,
                        "web_search": bool(web_search),
                    }
                    if file_base64:
                        payload["file_base64"] = file_base64
                    if file_name:
                        payload["file_name"] = file_name
                    response = await client.post(
                        f"{rag_base}/chat",
                        json=payload,
                    )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"RAG service unavailable: {exc}",
            ) from exc

        parsed = response.json()
        text = (parsed.get("response") or "").strip()
        model_name = (parsed.get("model") or "rag").strip()
        if not text:
            raise HTTPException(
                status_code=502,
                detail="RAG returned empty response",
            )
        sources = _normalize_sources(parsed.get("sources"))
        return AIChatResponse(response=text, model=model_name, sources=sources)

    ollama_url = settings.OLLAMA_URL.rstrip("/")

    body = {
        "model": settings.OLLAMA_MODEL,
        "messages": [{"role": "user", "content": message}],
        "stream": False,
        "options": {
            "num_ctx": settings.OLLAMA_NUM_CTX,
            "temperature": settings.OLLAMA_TEMPERATURE,
            "num_predict": settings.OLLAMA_NUM_PREDICT,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT_SECS) as client:
            response = await client.post(f"{ollama_url}/api/chat", json=body)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Model service unavailable: {exc}",
        ) from exc

    parsed = response.json()
    text = _extract_ollama_text(parsed).strip()
    if not text:
        raise HTTPException(
            status_code=502,
            detail="Model returned empty response",
        )

    return AIChatResponse(response=text, model=settings.OLLAMA_MODEL)
