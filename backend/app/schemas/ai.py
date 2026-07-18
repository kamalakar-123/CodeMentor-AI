from pydantic import BaseModel


class GenerateQuestionRequest(BaseModel):
    language: str
    difficulty: str
    question_type: str


class GenerateQuestionResponse(BaseModel):
    title: str
    description: str
    starter_code: str
    expected_output: str
    explanation: str