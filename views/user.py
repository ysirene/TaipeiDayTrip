import os
import datetime
import re

from dotenv import load_dotenv
import jwt

class TokenDataProcessor:

    @staticmethod
    def decode_token(auth_header):
        load_dotenv('../.env')
        secret_key = os.getenv('secret_key')
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return {'data': payload}
        except:
            return {'data': None}
        
    @staticmethod
    def encode_token(user_info):
        if user_info:
            load_dotenv('../.env')
            secret_key = os.getenv('secret_key')
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'id': user_info[0],
                'name': user_info[1],
                'email': user_info[2]
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            return {'token': token}, 200
        else:
            return {'error': True, 'message': 'incorrect email or password'}, 400

    @staticmethod
    def is_payload(data):
        if data['data'] != None:
            return data['data'], 200
        else:
            return {'error': True, 'message': 'not logged in'}, 403
        
class SignupDataChecker:

    @staticmethod
    def check_email(email):
        email_pattern = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
        if re.match(email_pattern, email):
            return {'ok': True}, 200
        else:
            return {'error': True, 'message': 'invalidate email'}, 400