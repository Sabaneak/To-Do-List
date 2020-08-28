from schemas.users import UserSchema
from models.users import  UserModel

import traceback
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from blacklist import BLACKLIST


user_schema = UserSchema()

class UserRegister(Resource):
    
    @classmethod
    def post(cls):
        try:
            person = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages

        if UserModel.find_by_username(person.username):
            return {'msg': 'Username {} already exists'.format(person.username)}

        if UserModel.find_by_email(person.email):
            return {'msg': 'Email {} already exists'.format(person.email)}
        
        try:
            person.save_to_data()
            person.send_confirmation_email()
            return {'msg': 'User created succesfully'}, 201

        except:
            person.delete_from_data()
            traceback.print_exc()
            return {'msg': "Internal Server Error"}, 500


class User(Resource):

    @classmethod
    def get(cls, user_id):
        person = UserModel.find_by_id(user_id)
        if not person:
            return {'msg': 'User with ID {} does not exist'.format(user_id)}
        return user_schema.dump(person)

    @classmethod
    def delete(cls, user_id):
        person = UserModel.find_by_id(user_id)
        if not person:
            return {'msg': 'User witih ID {} does not exist'.format(user_id)}
        
        person.delete_from_data()
        return {'msg': 'User deleted succesfully'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        person = user_schema.load(request.get_json())
        user_from_db = UserModel.find_by_username(person.username)

        if user_from_db and user_from_db.password == person.password:
            if user_from_db.activated:
                access_token = create_access_token(identity=user_from_db.id, fresh=True)
                refresh_token = create_refresh_token(user_from_db.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            
            return {'msg': "Email {} has not been confirmed".format(user_from_db.email)}

        return {'msg': 'Invalid Credentials'}


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'msg': 'User ID {} has been logged out'.format(user_id)}


class TokenRefresh(Resource):

    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}

class UserConfirm(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'msg': "User not found"}, 404

        user.activated = True
        user.save_to_data()
        return {'msg': "Registration has been confirmed for email {}".format(user.email)}
      

