from ..extensions import db
from .base import BaseModel

class Roles(BaseModel):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    users = db.relationship("User", back_populates="role")