from ..models.user_model import User
from ..extensions import db

class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def create(self, name, email):
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user