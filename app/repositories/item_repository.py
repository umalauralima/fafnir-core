from app.config import Config
from ..models.item_model import Item
from ..extensions import db
from sqlalchemy import insert, select

class ItemRepository:

    def get_all(self):
        return Item.query.all()
    
    def get_paginated(self, page: int = 1, per_page: int = Config.ITEMS_PER_PAGE):
        """
        Retorna uma página de resultados.
        """
        query = Item.query.order_by(Item.id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    def get_item_by_id(self, id):
        return Item.query.get(id)

    
    def delete_items(self, ids):
        try:
            db.session.query(Item).filter(Item.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise

    def create_items_bulk(self, items_data: list[dict]):
        
        try:
            for i in range(0, len(items_data), 100):
                batch = items_data[i:i + 100]

                stmt = insert(Item).values(batch)

                db.session.execute(stmt)

            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            raise

    def update(self, obj_id, data):
        try:
            obj = self.get_item_by_id(obj_id)

            if not obj:
                return None

            for key, value in data.items():
                setattr(obj, key, value)

            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()
            raise