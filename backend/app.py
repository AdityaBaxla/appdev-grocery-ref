from flask import Flask, jsonify
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

# @app.errorhandler(401)
# def unauthorized(error):
#     return jsonify({'message': 'Unauthorized - Authentication required'}), 401

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