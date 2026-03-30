from flask import Blueprint, g, jsonify, request
from pydantic import ValidationError
from app.decorators import get_token_data, requires_permission
from app.dto.items_dto import *
from app.services.item_service import ItemService
from ..dto.location_dto import *

items_bp = Blueprint("items", __name__)

service = ItemService()

@items_bp.route("/items", methods=["GET"])
@requires_permission("list_items")
def list():

    dto = ItemsListDTO(**request.args)

    pagination = service.list_items_paginated(dto.page)

    items = [ItemsListResponseDTO.model_validate(c).model_dump() for c in pagination["items"]]

    result = {
        "items": items,
        "total": pagination["total"],
        "page": pagination["page"],
        "per_page": pagination["per_page"],
        "pages": pagination["pages"],
        "has_next": pagination["has_next"],
        "has_prev": pagination["has_prev"]
    }

    return jsonify(result), 200

@items_bp.route("/items/create", methods=["POST"])
@requires_permission("create_items")
def create_items():
    user = g.current_user

    dto = ItemsCreateDTO(**request.json)
    response = service.create_items(dto, user)    

    return jsonify(response), 200


@items_bp.route("/items/delete", methods=["DELETE"])
@requires_permission("delete_items")
def delete_items():
    
    dto = ItemsDeleteDTO(**request.json)
    response = service.delete_items(dto.ids)    

    return jsonify(response), 200

@items_bp.route("/item/<int:id>", methods=["GET"])
@requires_permission("get_item")
def get_item(id):
    
    item = service.get_item(id)
    
    return ItemDetailDTO.model_validate(item).model_dump(), 201


@items_bp.route("/item/<int:id>", methods=["PUT"])
@requires_permission("update_item")
def update_item(id):

    # Cria DTO de entrada a partir do JSON
    dto = ItemUpdateDTO(**request.json)

    # Chama Service para atualizar
    obj = service.update_item(id, dto)

    # Converte para DTO de saída
    result = ItemDetailDTO.model_validate(obj).model_dump()

    return jsonify(result), 200