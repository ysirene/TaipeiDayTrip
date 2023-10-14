from flask import Blueprint, jsonify, request
from dotenv import load_dotenv

from models.user import UserDataFetcher
from views.user import UserDataProcessor

user = Blueprint('user', __name__)

# 註冊會員 POST
@user.route('/api/user', methods = ['POST'])
def signup():
	data = request.get_json()
	name = data.get('name')
	email = data.get('email')
	password = data.get('password')
	response, status_code = UserDataFetcher.signup(name, email, password)
	return jsonify(response), status_code

#  驗證會員 GET
@user.route(('/api/user/auth'), methods = ['GET'])
def verify_user():
	load_dotenv('../.env')
	auth_header = request.headers.get('Authorization')
	payload = UserDataProcessor.decode_token(auth_header)
	return jsonify(payload)
	
	
#  登入會員 PUT
@user.route(('/api/user/auth'), methods = ['PUT'])
def signin():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')
	response, status_code = UserDataFetcher.signin(email, password)
	if status_code != 200:
		return response, status_code
	else:
		token, status_code = UserDataProcessor.encode_token(response)
		return jsonify(token), status_code