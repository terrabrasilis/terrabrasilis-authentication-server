import jwt
import datetime
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

# The user entity
class User:
    
    id=None
    email=None
    password=None
    registered_on=None
    verified=False
    admin=False
        
    # read DOWNLOAD_API_SECRET from env file 
    env_path=(os.path.dirname(__file__) or '.') + '/.env'
    load_dotenv(dotenv_path=env_path)
    DOWNLOAD_API_SECRET=os.getenv("DOWNLOAD_API_SECRET")
    
    EXPIRATION_DAY=1
    # x hours * 60 min * 60 sec (default 8 hours)
    EXPIRATION_SECONDS=0#8 * 60 * 60

    #constructor
    def __init__(self, id, email, password, registered_on, verified=False, admin=False):
        self.id=id
        self.email=email
        self.password=password
        self.registered_on=registered_on.isoformat()
        self.verified=verified
        self.admin=admin


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=self.EXPIRATION_DAY, seconds=self.EXPIRATION_SECONDS),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                #self.SECRET_KEY,
                self.DOWNLOAD_API_SECRET,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer to a valid payload sub or string if error message
        """
        try:
            #payload = jwt.decode(auth_token, User.SECRET_KEY)
            payload = jwt.decode(auth_token, User.DOWNLOAD_API_SECRET)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'