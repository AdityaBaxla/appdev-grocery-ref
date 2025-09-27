from flask_security.utils import verify_password
from models import User
from services.errors import InvalidInputError, InvalidEmailError, WrongPasswordError

class AuthService:
    @staticmethod
    def login(email, password):
        if not email or not password:
            raise InvalidInputError("Missing email or password")
 
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
