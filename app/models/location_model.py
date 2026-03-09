from ..extensions import db
from .base import BaseModel

class Location(BaseModel):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    items = db.relationship("Item", backref="location", lazy=True)