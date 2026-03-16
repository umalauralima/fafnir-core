from app.repositories.location_repository import LocationRepository
from ..dto.location_dto import *


class LocationService:

    def __init__(self):
        self.repository = LocationRepository()

    def list_all(self):
        return self.repository.get_all()

    def get(self, location_id):
        obj = self.repository.get_by_id(location_id)

        if not obj:
            raise ValueError("Localidade não encontrada")

        return obj

    def create(self, dto: LocationCreateDTO):
        data = dto.model_dump(exclude_none=True)       
        return self.repository.create(data)

    def update_category(self, location_id, dto: LocationUpdateDTO):

        obj = self.repository.get_by_id(location_id)

        if not obj:
            raise ValueError("Categoria não encontrada")

        data = dto.model_dump(exclude_unset=True)
        self.repository.update(location_id, data)

        return obj

    def delete(self, obj_id):

        deleted = self.repository.delete(obj_id)

        if not deleted:
            raise ValueError("Localidade não encontrada")

        return True
    
    def list_locations_paginated(self, page: int = 1, per_page: int = 10):
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