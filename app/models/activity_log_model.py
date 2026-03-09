from datetime import datetime
from ..extensions import db
from .base import BaseModel


class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    action = db.Column(db.String(100))
    entity = db.Column(db.String(100))
    entity_id = db.Column(db.Integer)

    ip_address = db.Column(db.String(45))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)