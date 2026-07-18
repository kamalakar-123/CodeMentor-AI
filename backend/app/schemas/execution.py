from pydantic import BaseModel


class ExecutionResponse(BaseModel):
    submission_id: int
    status: str
    stdout: str
    stderr: str
    execution_time: float