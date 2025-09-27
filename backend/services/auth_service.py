from flask_security.utils import verify_password, hash_password
from services.errors import InvalidInputError, InvalidEmailError, WrongPasswordError, ServiceError
from flask import current_app


class AuthService:
    @staticmethod
    def get_datastore():
        return current_app.datastore

    @classmethod
    def login(cls, email, password):
        if not email or not password:
            raise InvalidInputError("Missing email or password")
        from models import User
        user = User.query.filter_by(email=email).first()
        if not user:
            raise InvalidEmailError("Invalid email")

        if not verify_password(password, user.password):
            raise WrongPasswordError("Wrong password")

        return {
            "token": user.get_auth_token(),
            "email": user.email,
            "role": user.roles[0].name if user.roles else None,
            "id": user.id,
        }

    @classmethod
    def register(cls, name, email, password, role):
        datastore = cls.get_datastore()
        from models import Role
        from extensions import db
        if not name or not email or not password or not role:
            raise InvalidInputError()
        
        role = Role.query.filter_by(name = role).first()
        if not role:
            raise InvalidInputError()
        active = True
        if role.name == "manager":
            active = False
        elif role.name == "admin":
            raise ServiceError("not allowed")

        try:
            user = datastore.create_user(name = name, password = hash_password(password), email = email)
            datastore.add_role_to_user(user, role)
            db.session.commit()
        except:
            db.session.rollback()

        return {"id": user.id, "email": user.email, "name": user.name, "role": user.roles[0].name}