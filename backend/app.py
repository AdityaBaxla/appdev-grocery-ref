from flask import Flask, jsonify
from services.errors import InvalidEmailError, ServiceError, WrongPasswordError
from resources.errors import ResourceError, InvalidDataError
from config import LocalDevelopmentConfig


from flask_security.decorators import auth_required

from flask_security.datastore import SQLAlchemyUserDatastore
from extensions import db, security

def create_app():

    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    from models import User, Role
    #flask security
    datastore = SQLAlchemyUserDatastore(db, User, Role)

    security.init_app(app, datastore=datastore, register_blueprint=False)
    app.datastore = datastore
    

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


    from resources import auth_bp, api_bp


    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(api_bp)
    return app

    # app.app_context().push()
app = create_app()

if (__name__ == "__main__"):
    app.run(debug=True)