from typing import Optional
from pydantic import BaseModel, Field


class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=120)

class UserUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)

    class Config:
        from_attributes = True

class UserResponseDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserSummaryDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True