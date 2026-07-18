from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestCaseBase(BaseModel):
    question_id: int
    input_data: str
    expected_output: str
    is_hidden: bool = False


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    input_data: str | None = None
    expected_output: str | None = None
    is_hidden: bool | None = None


class TestCaseResponse(TestCaseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)