from fastapi import APIRouter

from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import chat_with_model

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(payload: AIChatRequest):
    return await chat_with_model(payload)
