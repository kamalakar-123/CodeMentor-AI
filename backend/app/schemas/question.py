from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    language: str
    question_type: str
    starter_code: str = ""
    expected_output: str = ""
    explanation: str = ""
    ai_generated: bool = False


class QuestionUpdate(BaseModel):
    title: str
    description: str
    difficulty: str
    language: str
    question_type: str
    starter_code: str
    expected_output: str
    explanation: str
    ai_generated: bool


class QuestionResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    language: str
    question_type: str
    starter_code: str
    expected_output: str
    explanation: str
    ai_generated: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
