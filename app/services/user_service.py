from ..repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, dto):

        return self.repo.create(dto.name, dto.email)

    def list_users(self):

        return self.repo.get_all()