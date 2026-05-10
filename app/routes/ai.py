from fastapi import APIRouter, Request

from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_chat_parse import parse_ai_chat_request
from app.services.ai_service import chat_with_model

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


_AI_CHAT_JSON_SCHEMA = AIChatRequest.model_json_schema()


@router.post(
    "/chat",
    response_model=AIChatResponse,
    summary="Chat (JSON or multipart)",
    description=(
        "JSON: AIChatRequest with optional file_base64 + file_name (VirusTotal scan on RAG). "
        "Multipart: fields message, optional history (JSON string), optional file."
    ),
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": _AI_CHAT_JSON_SCHEMA,
                    "examples": {
                        "Tylko tekst": {
                            "summary": "Pytanie bez załącznika",
                            "value": {
                                "message": "co to jest phishing?",
                                "history": [],
                            },
                        },
                        "Z wyszukiwaniem w sieci": {
                            "summary": "Wymuszone web_search (DuckDuckGo)",
                            "value": {
                                "message": "co nowego w cyberbezpieczeństwie w tym tygodniu?",
                                "history": [],
                                "web_search": True,
                            },
                        },
                        "Z historią": {
                            "summary": "Kontynuacja rozmowy",
                            "value": {
                                "message": "rozwiń pierwszy punkt",
                                "history": [
                                    {"role": "user", "content": "wymień 3 oznaki phishingu"},
                                    {"role": "assistant", "content": "1) ..., 2) ..., 3) ..."},
                                ],
                            },
                        },
                        "Z plikiem (base64)": {
                            "summary": "Z załącznikiem do skanu VT",
                            "value": {
                                "message": "czy ten plik jest bezpieczny?",
                                "history": [],
                                "file_base64": "<BASE64_OF_FILE_BYTES>",
                                "file_name": "suspicious.exe",
                            },
                        },
                    },
                },
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["message"],
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "User message sent to the model",
                            },
                            "history": {
                                "type": "string",
                                "description": (
                                    "Optional JSON-encoded array of "
                                    "{role: 'user'|'assistant', content: '...'} turns"
                                ),
                            },
                            "file": {
                                "type": "string",
                                "format": "binary",
                                "description": "Optional attachment — forwarded to RAG → VirusTotal",
                            },
                            "web_search": {
                                "type": "string",
                                "enum": ["true", "false"],
                                "description": "If 'true', RAG runs DuckDuckGo web_search on the message",
                            },
                            "locale": {
                                "type": "string",
                                "description": "UI locale (pl or en) for in-app wiki/quiz links in the reply",
                            },
                        },
                    },
                },
            },
        },
    },
)
async def ai_chat(request: Request):
    message, history, upload, fb64, fname, web_search, locale = await parse_ai_chat_request(request)
    return await chat_with_model(
        message, history, upload, fb64, fname, web_search=web_search, locale=locale
    )
