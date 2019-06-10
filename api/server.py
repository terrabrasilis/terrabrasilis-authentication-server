import os
from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from storage_module.user_dao import UserDao
from storage_module.blacklist_dao import BlacklistDao
from storage_module.user import User

SERVER_IP='0.0.0.0'
BCRYPT_LOG_ROUNDS=13

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)

api = Api(app)

class UserRegister(Resource):
    """
    The entry point to register Users.
    """
    def post(self):
        # set default
        json_data=None

        # Trying parse the input JSON
        try:
            json_data = request.get_json()
        except Exception as error:
            return {'status':'fail','message': 'invalid input data'}, 500
        
        # trying store data into database
        try:
            db = UserDao()
            user = db.getUserBy(json_data.get('email'))
            if not user:
                password = bcrypt.generate_password_hash(json_data['password'], BCRYPT_LOG_ROUNDS).decode()
                id_user = db.storeUser(json_data['email'],password)
            else:
                # HTTP 409: Conflict
                return {'status':'fail','message':'Email already registered'}, 409
        except Exception as error:
            return {'status':'fail','message': 'internal error in API registry'}, 500
        
        return {'status':'success','message': 'Completed'}, 201

class Login(Resource):
    """
    User Login. Use to obtain one token based on user credentials.
    """
    def post(self):
       # set default
        json_data=None

        # Trying parse the input JSON
        try:
            json_data = request.get_json()
        except Exception as error:
            return {'status':'fail','message': 'invalid input data'}, 500
        
        try:
            db = UserDao()
            # fetch the user data
            user = db.getUserBy(json_data.get('email'))
            if user and bcrypt.check_password_hash(
                user.password, json_data.get('password')
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return responseObject, 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return responseObject, 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


class CheckAuthorization(Resource):
    """
    User Resource to check if Authorization is valid
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return responseObject, 401
        else:
            auth_token = ''
        if auth_token:
            id_or_error_msg = User.decode_auth_token(auth_token)
            if not isinstance(id_or_error_msg, str):
                db = UserDao()
                # fetch the user data by ID
                user = db.getUserBy(id_or_error_msg)
                if user and user.verified:
                    responseObject = {
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'email': user.email,
                            'admin': user.admin,
                            'registered_at': user.registered_on
                        }
                    }
                    return responseObject, 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Missing validate email'
                    }
                    return responseObject, 401
            responseObject = {
                'status': 'fail',
                'message': id_or_error_msg
            }
            return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return responseObject, 401


class Logout(Resource):
    """
    Invalidate tokens to guarantee the log out by putting on in blacklist table.

    TODO: Discard expired tokens from blacklist tokens to keep the database table clear.
    """
    def get(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                
                try:
                    db = BlacklistDao()

                    is_blacklisted_token = db.tokenIsBlacklisted(auth_token)
                    if is_blacklisted_token:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Token blacklisted. Please log in again.'
                        }
                        return responseObject, 401
                    else:
                        # mark the token as blacklisted
                        blacklist_token_id = db.storeToken(token=auth_token)
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged out.'
                        }
                        return responseObject, 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return responseObject, 401
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return responseObject, 403

api.add_resource(UserRegister, '/register')
api.add_resource(Login, '/login')
api.add_resource(CheckAuthorization, '/isAuthorized')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(host=SERVER_IP, port=5000, Debug=True)