from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message sent to the model")


class AIChatResponse(BaseModel):
    response: str
    model: str
