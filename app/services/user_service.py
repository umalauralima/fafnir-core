from app.errors.error_handler import ErrorHandler
from ..repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def get_user_from_token(self, payload):
        auth_id = payload.get("sub")

        if not auth_id:
            ErrorHandler.unauthorized("Token inválido")

        user = self.repo.get_by_email(payload.get("email"))

        if not user:
            ErrorHandler.unauthorized("Usuário não encontrado")

        return user

    def create_user(self, dto):

        return self.repo.create(dto.name, dto.email)

    def list_users(self):

        return self.repo.get_all()