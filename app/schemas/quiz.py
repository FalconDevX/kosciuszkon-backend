from datetime import datetime

from pydantic import BaseModel


class QuizQuestionResponse(BaseModel):
    id: int

    category: str
    difficulty: str

    question: str

    answer_a: str
    answer_b: str
    answer_c: str
    answer_d: str

    created_at: datetime

    class Config:
        from_attributes = True
