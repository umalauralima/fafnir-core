
# Listar OK
# Detalhe da request OK
# Criar request OK
# Aceitar request
# Recusar request
# Cancelar request
# Apagar request

from ..extensions import db
from ..config import Config
from ..models.request_model import *

class RequestsRepository:

    def get_all(self):
        return Request.query.all()
    
    def get_by_id(self, id):
        return Request.query.get(id)
    
    def get_paginated(self, page: int = 1, per_page: int = Config.ITEMS_PER_PAGE):
        
        query = Request.query.order_by(Request.id)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination

    def create_request(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()
            raise

    def approve_request(self, obj_id):
        try:
            obj = self.get_item_by_id(obj_id)

            if not obj:
                raise ValueError("Objeto não encontrado")

            obj.status = "APPROVED"
            obj.approved_at = datetime.utcnow

            db.session.commit()

            return obj
        
        except Exception:
            db.session.rollback()
            raise

    def rejected_request(self, obj_id):
        try:
            obj = self.get_item_by_id(obj_id)

            if not obj:
                raise ValueError("Objeto não encontrado")

            obj.status = "REJECTED"
            obj.rejected_at = datetime.utcnow

            db.session.commit()

            return obj
        
        except Exception:
            db.session.rollback()
            raise

    def cancel_request(self, obj_id):
        try:
            obj = self.get_by_id(obj_id)

            if not obj:
                raise ValueError("Objeto não encontrado")

            obj.status = "CANCELLED"
            obj.canceled_at = datetime.utcnow

            db.session.commit()

            return obj
        
        except Exception:
            db.session.rollback()
            raise

    def delete(self, obj_id):
        try:
            obj = self.get_by_id(obj_id)

            if not obj:
                return False

            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def add(self, obj):
        db.session.add(obj)