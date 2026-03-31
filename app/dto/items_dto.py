from typing import Optional
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class ItemsListDTO(BaseModel):
    page: int = Field(..., ge=1)
    per_page: int = Field(..., ge=1, le=100)

class ItemsListResponseDTO(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    stock_total: int
    stock_reserved: int

    class Config:
        from_attributes = True

class ItemDetailDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_id: int
    unit_id: int
    location_id: int
    stock_total: int
    minimum_stock: int

    class Config:
        from_attributes = True
    
class ItemCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None

    category_id: int
    unit_id: int
    location_id: int

    stock: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_stock(self):
        if self.minimum_stock > self.stock:
            raise ValueError("minimum_stock cannot be greater than stock")
        return self

class ItemUpdateDTO(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None

    stock: Optional[int] = Field(None, ge=0)
    minimum_stock: Optional[int] = Field(None, ge=0)

    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    location_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_stock(self):
        if (
            self.minimum_stock is not None and
            self.stock is not None and
            self.minimum_stock > self.stock
        ):
            raise ValueError("minimum_stock cannot be greater than quantity")
        return self

class ItemsCreateDTO(BaseModel):
    items: List[ItemCreateDTO] = Field(..., min_items=1)

class ItemsDeleteDTO(BaseModel):
    ids: List[int] = Field(..., min_ids=1)

    class Config:
        from_attributes = True

class SummaryRequestItemDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True