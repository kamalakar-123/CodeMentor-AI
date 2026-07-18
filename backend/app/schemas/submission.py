from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubmissionCreate(BaseModel):
    question_id: int
    language: str
    source_code: str


class SubmissionUpdate(BaseModel):
    status: str


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    language: str
    source_code: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)