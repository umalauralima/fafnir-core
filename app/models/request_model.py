from datetime import datetime
from ..extensions import db
from .base import BaseModel

class Request(BaseModel):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)

    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    approved_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    requester = db.relationship(
        "User",
        foreign_keys=[requester_id],
        back_populates="requested_items"
    )

    approver = db.relationship(
        "User",
        foreign_keys=[approved_by_id],
        back_populates="approved_requests"
    )

    status = db.Column(
        db.Enum(
            "PENDING",
            "APPROVED",
            "REJECTED",
            "CANCELLED",
            "COMPLETED",
            name="request_status"
        ),
        default="PENDING"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    canceled_at = db.Column(db.DateTime, nullable=True)

    items = db.relationship("RequestItem", back_populates="request", lazy=True)