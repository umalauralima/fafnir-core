from ..extensions import db
from .base import BaseModel

class Unit(BaseModel):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)

    items = db.relationship("Item", backref="unit", lazy=True)