from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.errors.base import ApiError


class ErrorHandler:

    # =========================
    # REGISTRO GLOBAL
    # =========================
    @classmethod
    def init_app(cls, app):

        @app.errorhandler(ApiError)
        def handle_api_error(e):
            return jsonify({
                "error": {
                    "code": e.code,
                    "message": e.message
                }
            }), e.status_code

        @app.errorhandler(ValidationError)
        def handle_validation_error(e):
            errors = e.errors()

            missing = []
            invalid = []

            for err in errors:
                field = err["loc"][0]

                if err["type"] == "missing":
                    missing.append(field)
                else:
                    invalid.append({
                        "field": field,
                        "message": err["msg"]
                    })

            if missing:
                return jsonify({
                    "error": {
                        "code": "REQ-001",
                        "message": "Campos obrigatórios não informados",
                        "fields": missing
                    }
                }), 400

            return jsonify({
                "error": {
                    "code": "REQ-002",
                    "message": "Dados inválidos",
                    "details": invalid
                }
            }), 400

        @app.errorhandler(IntegrityError)
        def handle_integrity_error(e):
            return jsonify({
                "error": {
                    "code": "DB-001",
                    "message": "Violação de integridade no banco"
                }
            }), 409

        @app.errorhandler(HTTPException)
        def handle_http_exception(e):
            return jsonify({
                "error": {
                    "code": f"HTTP-{e.code}",
                    "message": e.description
                }
            }), e.code

        @app.errorhandler(Exception)
        def handle_generic_error(e):
            print(f"[ERROR] {str(e)}")

            return jsonify({
                "error": {
                    "code": "SYS-001",
                    "message": "Erro interno do servidor"
                }
            }), 500

    # =========================
    # MÉTODOS DE ERRO
    # =========================

    @staticmethod
    def not_found(resource="Recurso"):
        raise ApiError(
            code="RES-404",
            message=f"{resource} não encontrado",
            status_code=404
        )

    @staticmethod
    def bad_request(message="Requisição inválida"):
        raise ApiError(
            code="REQ-002",
            message=message,
            status_code=400
        )

    @staticmethod
    def conflict(message="Conflito de dados"):
        raise ApiError(
            code="DB-001",
            message=message,
            status_code=409
        )

    @staticmethod
    def unauthorized():
        raise ApiError(
            code="AUTH-401",
            message="Não autorizado",
            status_code=401
        )

    @staticmethod
    def internal():
        raise ApiError(
            code="SYS-001",
            message="Erro interno do servidor",
            status_code=500
        )
    
    @staticmethod
    def missing_header(header_name: str):
        raise ApiError(
            code="REQ-003",
            message=f"Header não informado: {header_name}",
            status_code=400
        )