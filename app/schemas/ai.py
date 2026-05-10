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
    web_search: bool = Field(
        default=False,
        description="If true, instruct RAG to run a DuckDuckGo web search on the message and feed snippets to the model.",
    )
    locale: str | None = Field(
        default=None,
        description="UI locale (pl or en) so the assistant can link to wiki/quiz routes for the active language.",
    )


class AISource(BaseModel):
    title: str
    url: str


class AIChatResponse(BaseModel):
    response: str
    model: str
    sources: list[AISource] = Field(default_factory=list)
