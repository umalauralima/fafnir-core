from datetime import datetime
from ..extensions import db
from .base import BaseModel

class InventoryMovement(BaseModel):
    __tablename__ = "inventory_movements"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"))

    type = db.Column(
        db.Enum(
            "ENTRY",
            "EXIT",
            "RETURN",
            "ADJUSTMENT",
            "RESERVE",
            name="movement_type"
        ),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    previous_quantity = db.Column(db.Integer)
    new_quantity = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)