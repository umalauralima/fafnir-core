from app.config import Config
from ..repositories.item_repository import ItemRepository
from ..dto.items_dto import *

class ItemService:

    def __init__(self):
        self.repository = ItemRepository()

    def list_items(self):

        return self.repository.get_all()

    def get_item(self, id):
        return self.repository.get_item_by_id(id)
        
    def create_items(self, dto, user):

        # 1. montar payload
        items_data = [
            {
                "name": item.name,
                "description": item.description,
                "category_id": item.category_id,
                "unit_id": item.unit_id,
                "location_id": item.location_id,
                "quantity": item.quantity,
                "minimum_stock": item.minimum_stock,
                "created_by": user.id
            }
            for item in dto.items
        ]

        self.repository.create_items_bulk(items_data)

        return {
            "message": "Items created successfully",
            "count": len(items_data)
        }
    
    def delete_items(self, ids):
        result = self.repository.delete_items(ids)

        return {
            "message": "Items deleted successfully"
        }
    
    def list_items_paginated(self, page: int = 1, per_page: int = Config.ITEMS_PER_PAGE):
        pagination = self.repository.get_paginated(page, per_page)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    
    def update_item(self, obj_id, dto: ItemUpdateDTO):

        obj = self.repository.get_item_by_id(obj_id)

        if not obj:
            raise ValueError("Item não encontrada")
        
        for field in dto.model_fields_set:
            setattr(obj, field, getattr(dto, field))

        data = dto.model_dump(exclude_unset=True)
        self.repository.update(obj_id, data)

        return obj
