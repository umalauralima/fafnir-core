import traceback

import jwt
from flask import request, jsonify
from functools import wraps

from app.config import Config
from app.errors.error_handler import ErrorHandler

def get_token_data():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        ErrorHandler.bad_request()

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                payload = get_token_data()
            except Exception as e:
                print(traceback.format_exc())
                ErrorHandler.internal()

            if permission not in payload.get("permissions", []):
                ErrorHandler.unauthorized()

            return f(*args, **kwargs)

        return wrapper
    return decorator