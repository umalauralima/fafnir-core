from datetime import datetime
from ..extensions import db
from .base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))

    quantity = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer, default=0)

    expiration_date = db.Column(db.Date)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    movements = db.relationship("InventoryMovement", backref="item", lazy=True)