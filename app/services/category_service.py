from app.repositories.category_repository import CategoryRepository
from ..dto.category_dto import *


class CategoryService:

    def __init__(self):
        self.repository = CategoryRepository()

    def list_categories(self):
        return self.repository.get_all()

    def get_category(self, category_id):
        category = self.repository.get_by_id(category_id)

        if not category:
            raise ValueError("Categoria não encontrada")

        return category

    def create_category(self, dto: CategoryCreateDTO):
        data = dto.model_dump(exclude_none=True)       
        return self.repository.create(data)

    def update_category(self, category_id, dto: CategoryUpdateDTO):

        category = self.repository.get_by_id(category_id)

        if not category:
            raise ValueError("Categoria não encontrada")

        data = dto.model_dump(exclude_unset=True)  # pega só os campos enviados     
        self.repository.update(category_id, data)

        return category

    def delete_category(self, category_id):

        deleted = self.repository.delete(category_id)

        if not deleted:
            raise ValueError("Categoria não encontrada")

        return True
    
    def list_categories_paginated(self, page: int = 1, per_page: int = 10):
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