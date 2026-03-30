import traceback
from flask import g
import jwt
from flask import request, jsonify
from functools import wraps
from .services.user_service import UserService

from app.config import Config
from app.errors.error_handler import ErrorHandler

def get_token_data():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        ErrorHandler.bad_request()

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        ErrorHandler.unauthorized("Token expirado")

    except jwt.InvalidTokenError:
        ErrorHandler.unauthorized("Token inválido")


def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            user_service = UserService()

            payload = get_token_data()
            user = user_service.get_user_from_token(payload)

            # guarda no contexto da request
            g.current_user = user

            ## TODO Validar depois de acrescentar as permissões no banco
            """if permission not in payload.get("permissions", []):
                ErrorHandler.unauthorized("Permissão insuficiente")"""

            return f(*args, **kwargs)

        return wrapper
    return decorator