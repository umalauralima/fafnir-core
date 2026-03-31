from ..extensions import db
class RequestItemRepository:

    def __init__(self, model):
        self.model = model

    def add_all(self, items):
        db.session.add_all(items)