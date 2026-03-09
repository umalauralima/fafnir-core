from datetime import datetime
from ..extensions import db
from .base import BaseModel

class Alert(BaseModel):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    type = db.Column(
        db.Enum(
            "LOW_STOCK",
            "EXPIRING",
            "EXPIRED",
            name="alert_type"
        )
    )

    message = db.Column(db.String(255))
    resolved = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)