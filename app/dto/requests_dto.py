from datetime import datetime, timezone
from typing import List
import zoneinfo
from pydantic import BaseModel, Field, field_serializer

from enum import Enum
from app.dto.items_dto import SummaryRequestItemDTO

from app.dto.user_dto import UserSummaryDTO

class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class RequestListResponseDTO(BaseModel):
    
    id: int
    requester_id: int
    approved_by_id: int | None
    status: RequestStatus
    created_at: datetime

    class Config:
        from_attributes = True

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        if not value:
            return value

        # 🔥 Se vier sem timezone, assume UTC
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        # timezone da máquina (ex: Brasil)
        local_tz = zoneinfo.ZoneInfo("America/Manaus")

        local_dt = value.astimezone(local_tz)

        return local_dt.strftime("%d/%m/%Y %H:%M:%S")

class RequestDetailDTO(BaseModel):
    id: int

    requester: UserSummaryDTO
    approver: UserSummaryDTO | None

    status: RequestStatus

    created_at: datetime
    approved_at: datetime | None
    rejected_at: datetime | None
    canceled_at: datetime | None

    items: list[SummaryRequestItemDTO]

    class Config:
        from_attributes = True

class RequestItemCreateDTO(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    item_id: int
    quantity: int

class RequestCreateDTO(BaseModel):
    items: List[RequestItemCreateDTO] = Field(..., min_items=1)

class RequestApproveDTO(BaseModel):
    approved_by_id: int

class RequestRejectDTO(BaseModel):
    reason: str | None = None