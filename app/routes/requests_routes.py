from flask import Blueprint, g, jsonify, request
from app.decorators import requires_permission
from app.dto.requests_dto import RequestCreateDTO, RequestDetailDTO, RequestListResponseDTO
from app.services.requests_service import RequestsService

requests_bp = Blueprint("requests", __name__)
service = RequestsService()

@requests_bp.route("/requests", methods=["GET"])
@requires_permission("list_req")
def list_requests():

    page = request.args.get("page", default=1, type=int)
    pagination = service.list_requests_paginated(page)

    items = [RequestListResponseDTO.model_validate(c).model_dump() for c in pagination["items"]]

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

@requests_bp.route("/requests", methods=["POST"])
@requires_permission("create_req")
def create():

    dto = RequestCreateDTO(**request.json)

    req = service.create(dto, g.current_user.id)

    return RequestDetailDTO.model_validate(req).model_dump(), 201

@requests_bp.route("/requests/<int:id>", methods=["GET"])
@requires_permission("get_req")
def get_item(id):
    
    item = service.get_item_by_id(id)
    
    return RequestDetailDTO.model_validate(item).model_dump(), 201