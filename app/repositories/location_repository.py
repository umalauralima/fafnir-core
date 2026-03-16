from app.config import Config
from ..models.location_model import Location
from ..extensions import db

class LocationRepository:

    def get_all(self):
        return Location.query.all()

    def get_by_id(self, obj_id):
        return Location.query.get(obj_id)

    def create(self, data):
        try:
            obj = Location(**data)
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()
            raise

    def update(self, obj_id, data):
        try:
            obj = self.get_by_id(obj_id)

            if not obj:
                return None

            for key, value in data.items():
                setattr(obj, key, value)

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

    def get_paginated(self, page: int = 1, per_page: int = Config.LOCATIONS_PER_PAGE):
        """
        Retorna uma página de resultados.
        """
        query = Location.query.order_by(Location.id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination