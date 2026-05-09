from fastapi import APIRouter, Request

from app.schemas.ai import AIChatResponse
from app.services.ai_chat_parse import parse_ai_chat_request
from app.services.ai_service import chat_with_model

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/chat",
    response_model=AIChatResponse,
    summary="Chat (JSON or multipart)",
    description=(
        "JSON: AIChatRequest with optional file_base64 + file_name (VirusTotal scan on RAG). "
        "Multipart: fields message, optional history (JSON string), optional file."
    ),
)
async def ai_chat(request: Request):
    message, history, upload, fb64, fname = await parse_ai_chat_request(request)
    return await chat_with_model(message, history, upload, fb64, fname)
