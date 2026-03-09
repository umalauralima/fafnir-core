import datetime
from ..extensions import db
from .base import BaseModel

class User(BaseModel):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Roles", back_populates="users")
    
    requested_items = db.relationship(
        "Request",
        foreign_keys="Request.requester_id",
    )

    approved_requests = db.relationship(
        "Request",
        foreign_keys="Request.approved_by_id",
    )
