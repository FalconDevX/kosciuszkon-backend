from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message sent to the model")
    history: list[dict[str, str]] = Field(
        default_factory=list,
        description="Optional chat turns for RAG (roles: user | assistant)",
    )
    file_base64: str | None = Field(
        default=None,
        description="Optional file as standard base64 — forwarded to RAG → VirusTotal file scan",
    )
    file_name: str | None = Field(
        default=None,
        description="Original filename when using file_base64",
    )


class AIChatResponse(BaseModel):
    response: str
    model: str
