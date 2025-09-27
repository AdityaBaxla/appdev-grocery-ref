from flask import request, jsonify, Blueprint
from flask_security.utils import verify_password
from models import User
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message" : "invalid inputs"}), 404
    
    return AuthService.login(email, password)