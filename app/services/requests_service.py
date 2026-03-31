from collections import defaultdict
from app.dto.requests_dto import RequestCreateDTO
from app.models.request_item_model import RequestItem
from app.repositories.item_repository import ItemRepository
from app.repositories.request_item_repository import RequestItemRepository
from app.repositories.requests_repository import RequestsRepository
from ..models.request_model import Request
from ..extensions import db

class RequestsService:
    def __init__(self):
        self.repository = RequestsRepository()
        self.request_item_repository = RequestItemRepository(model=RequestItem)
        self.item_repository = ItemRepository()
        self.db = db

    def list_requests_paginated(self, page: int = 1, per_page: int = 10):
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
    
    def create(self, dto, requester_id: int):
        try:
            
            item_ids = [i.item_id for i in dto.items]

            # Buscar com lock
            items_db = self.item_repository.get_by_ids_for_update(item_ids)
            items_db_map = {item.id: item for item in items_db}

            # Validar tudo
            for item_dto in dto.items:

                item_db = items_db_map.get(item_dto.item_id)

                if not item_db:
                    raise ValueError(f"Item {item_dto.item_id} não encontrado")

                if item_dto.quantity <= 0:
                    raise ValueError("Quantidade inválida")

                if item_db.stock_available < item_dto.quantity:
                    raise ValueError(
                        f"Estoque insuficiente para item {item_db.name}"
                    )

            # Faz a reserva
            for item_dto in dto.items:
                item = items_db_map[item_dto.item_id]
                item.stock_reserved += item_dto.quantity

            # Cria request
            request = Request(
                requester_id=requester_id,
                status="PENDING"
            )

            self.repository.add(request)
            self.db.session.flush()

            request_items = [
                self.request_item_repository.model(
                    request=request,
                    item_id=i.item_id,
                    quantity_requested=i.quantity
                )
                for i in dto.items
            ]

            self.request_item_repository.add_all(request_items)

            self.db.session.commit()

            return request

        except Exception:
            self.db.session.rollback()
            raise
