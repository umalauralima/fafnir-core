from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.services.category_service import CategoryService
from ..dto.category_dto import *

category_bp = Blueprint("categories", __name__)

service = CategoryService()

@category_bp.route("/categories", methods=["GET"])

def list_categories():

    page = request.args.get("page", default=1, type=int)
    pagination = service.list_categories_paginated(page)

    items = [CategoryResponseDTO.model_validate(c).model_dump() for c in pagination["items"]]

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

@category_bp.route("/categories", methods=["POST"])
def create_category():

    try:
        dto = CategoryCreateDTO(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = service.create_category(dto)

    return CategoryResponseDTO.model_validate(category).model_dump(), 201

@category_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    try:
        
        category = service.get_category(category_id)

        # Converte ORM para DTO
        dto = CategoryResponseDTO.model_validate(category).model_dump()

        return jsonify(dto), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500
    
@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    try:
        # Cria DTO de entrada a partir do JSON
        dto = CategoryUpdateDTO(**request.json)

        # Chama Service para atualizar
        category = service.update_category(category_id, dto)

        # Converte para DTO de saída
        result = CategoryResponseDTO.model_validate(category).model_dump()

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500
    
@category_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    try:
        
        service.delete_category(category_id)
        return jsonify({"message": "Categoria removida com sucesso"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "Erro interno"}), 500