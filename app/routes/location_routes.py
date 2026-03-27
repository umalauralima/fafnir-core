from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.decorators import requires_permission
from app.services.location_service import LocationService
from ..dto.location_dto import *

location_bp = Blueprint("locations", __name__)

service = LocationService()

@location_bp.route("/locations", methods=["GET"])
@requires_permission("list_loc")
def list():

    page = request.args.get("page", default=1, type=int)
    pagination = service.list_locations_paginated(page)

    items = [LocationResponseDTO.model_validate(c).model_dump() for c in pagination["items"]]

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

@location_bp.route("/locations", methods=["POST"])
@requires_permission("create_loc")
def create():

    dto = LocationCreateDTO(**request.json)

    location = service.create(dto)

    return LocationResponseDTO.model_validate(location).model_dump(), 201

@location_bp.route("/locations/<int:location_id>", methods=["GET"])
@requires_permission("get_loc")
def get_location(location_id):
    try:
        
        location = service.get(location_id)

        # Converte ORM para DTO
        dto = LocationResponseDTO.model_validate(location).model_dump()

        return jsonify(dto), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500
    
@location_bp.route("/locations/<int:location_id>", methods=["PUT"])
@requires_permission("update_loc")
def update(location_id):
    try:
        # Cria DTO de entrada a partir do JSON
        dto = LocationUpdateDTO(**request.json)

        # Chama Service para atualizar
        obj = service.update_category(location_id, dto)

        # Converte para DTO de saída
        result = LocationResponseDTO.model_validate(obj).model_dump()

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500
    
@location_bp.route("/locations/<int:location_id>", methods=["DELETE"])
@requires_permission("delete_loc")
def delete(location_id):
    try:
        
        service.delete(location_id)
        return jsonify({"message": "Localidade removida com sucesso"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500