import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.schemas.ai import AIChatRequest, AIChatResponse


def _extract_ollama_text(payload: dict) -> str:
    message = payload.get("message", {}) or {}
    return (
        message.get("content")
        or message.get("reasoning_content")
        or payload.get("response")
        or payload.get("output_text")
        or ""
    )


async def chat_with_model(data: AIChatRequest) -> AIChatResponse:
    rag_base = (settings.RAG_SERVICE_URL or "").strip().rstrip("/")
    if rag_base:
        try:
            async with httpx.AsyncClient(timeout=settings.RAG_TIMEOUT_SECS) as client:
                response = await client.post(
                    f"{rag_base}/chat",
                    json={"message": data.message},
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
        return AIChatResponse(response=text, model=model_name)

    ollama_url = settings.OLLAMA_URL.rstrip("/")

    body = {
        "model": settings.OLLAMA_MODEL,
        "messages": [{"role": "user", "content": data.message}],
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
