from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from ..services.user_service import UserService
from ..dto.user_dto import UserCreateDTO, UserResponseDTO

user_bp = Blueprint("users", __name__)

service = UserService()

@user_bp.route("/users", methods=["POST"])
def create_user():

    try:
        dto = UserCreateDTO(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    user = service.create_user(dto)

    return UserResponseDTO.model_validate(user).model_dump(), 201

@user_bp.route("/users", methods=["GET"])
def list_users():

    users = service.list_users()

    result = [
        UserResponseDTO.model_validate(u).model_dump()
        for u in users
    ]

    return jsonify(result)