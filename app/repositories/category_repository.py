from app.config import Config
from ..models.category_model import Category
from ..extensions import db

class CategoryRepository:

    def get_all(self):
        return Category.query.all()

    def get_by_id(self, obj_id):
        return Category.query.get(obj_id)

    def create(self, data):
        try:
            category = Category(**data)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception:
            db.session.rollback()
            raise

    def update(self, obj_id, data):
        try:
            category = self.get_by_id(obj_id)

            if not category:
                return None

            for key, value in data.items():
                setattr(category, key, value)

            db.session.commit()
            return category
        except Exception:
            db.session.rollback()
            raise

    def delete(self, obj_id):
        try:
            category = self.get_by_id(obj_id)

            if not category:
                return False

            db.session.delete(category)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    def get_paginated(self, page: int = 1, per_page: int = Config.CATEGORIES_PER_PAGE):
        """
        Retorna uma página de resultados.
        """
        query = Category.query.order_by(Category.id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination