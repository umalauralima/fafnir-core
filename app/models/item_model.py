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

    stock_total = db.Column(db.Integer, nullable=False)
    stock_reserved = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer, default=0)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    movements = db.relationship("InventoryMovement", backref="item", lazy=True)

    @property
    def stock_available(self):
        return self.stock_total - self.stock_reserved