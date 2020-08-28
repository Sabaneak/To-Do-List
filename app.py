import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError

from resources.users import (
    UserRegister, 
    User, UserLogin,
    UserLogout, 
    TokenRefresh, 
    UserConfirm,
)

from resources.tasks import Input_Tasks, Tasks, TasksList

from db import data
from mallow import ma
from blacklist import BLACKLIST

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]
app.secret_key = os.environ.get("APP_SECRET_KEY")

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def table():
    data.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages)

@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserConfirm, '/user_confirm/<int:user_id>')

api.add_resource(Input_Tasks, '/tasks')
api.add_resource(Tasks, '/tasks/<int:_id>')
api.add_resource(TasksList, '/tasks/all')


if __name__ == '__main__':
    data.init_app(app)
    ma.init_app(app)
    app.run(debug=True, use_reloader=False)