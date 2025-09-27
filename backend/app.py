from flask import Flask, jsonify
from services.errors import InvalidEmailError, ServiceError, WrongPasswordError
from resources.errors import ResourceError, InvalidDataError
from config import LocalDevelopmentConfig
from models import db, User, Role
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.core import Security
from flask_security.decorators import auth_required


app = Flask(__name__)

app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)

#flask security
datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, datastore=datastore, register_blueprint=False)

# Global error handlers
@app.errorhandler(ResourceError)
def handle_resource_error(error):
    code = 400
    if isinstance(error, InvalidDataError):
        code = 422
    return jsonify({"message": str(error)}), code

@app.errorhandler(ServiceError)
def handle_service_error(error):
    # Default to 400
    code = 400
    if isinstance(error, InvalidEmailError) or isinstance(error, WrongPasswordError):
        code = 401
    return jsonify({"message": str(error)}), code


from resources import auth_bp

# register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route('/login',endpoint='security.login', methods=['GET', 'POST'])
def login():
    return jsonify({'message': 'Authentication required'}), 401

@app.route('/')
def test():
    return {'message' : 'should be accessible'}

@app.route('/api/private')
@auth_required()
def private():
    return {"message" : "should not access"}

app.app_context().push()

if (__name__ == "__main__"):
    app.run(debug=True)