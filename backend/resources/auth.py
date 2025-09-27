from flask import request, jsonify, Blueprint
from flask_security.utils import verify_password
from resources.errors import InvalidDataError
from services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    print(f"email : {email}, pass: {password}")

    if not email or not password:
        raise InvalidDataError("missing /improper data")
    
    return AuthService.login(email, password)