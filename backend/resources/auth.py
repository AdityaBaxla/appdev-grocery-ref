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

@auth_bp.post("/register")
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password or not role:
        raise InvalidDataError()
    return AuthService.register(name, email, password, role)

@auth_bp.route("/logout", methods=['GET'])
def logout():
    return jsonify({"message" : "logged out"})















# /register	POST	Create a new user account. Body contains user info.
# /forgot-password	POST	Request password reset email. Body contains email.
# /reset-password	POST	Submit new password along with reset token.
# /change-password	POST	Authenticated route to change password.
# /refresh	POST	Exchange refresh token for new access token.
# /me or /profile	GET	Retrieve current authenticated user info.
# /verify-email	GET / POST	Verify email using a token from link. POST if sending token in body.
# /confirm-account	GET	Usually triggered by link in email.