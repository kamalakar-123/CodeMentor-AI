from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    email: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
