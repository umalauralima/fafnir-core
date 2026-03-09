from ..extensions import db
from .base import BaseModel

class RequestItem(BaseModel):
    __tablename__ = "request_items"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"))
    request = db.relationship("Request", back_populates="items")

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    quantity_requested = db.Column(db.Integer, nullable=False)
    quantity_approved = db.Column(db.Integer)
    quantity_delivered = db.Column(db.Integer)

    item = db.relationship("Item")