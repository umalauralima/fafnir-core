from pydantic import BaseModel, Field, field_validator
from typing import Optional


class CategoryCreateDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class CategoryUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=2, max_length=255)

    class Config:
        from_attributes = True


class CategoryResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

    # transforma None em string vazia
    @field_validator("description", mode="before")
    def none_to_empty(cls, v):
        if v is None:
            return ""
        return v