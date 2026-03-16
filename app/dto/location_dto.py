from typing import Optional
from pydantic import BaseModel, Field

class LocationCreateDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., max_length=255)

class LocationUpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=2, max_length=255)

    class Config:
        from_attributes = True

class LocationResponseDTO(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True