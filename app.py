from flask import *
import mysql.connector
import os
from dotenv import load_dotenv
import datetime
import jwt

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

def connect_to_db():
    load_dotenv()
    conn = mysql.connector.connect(
        host = 'localhost',
        database = 'tripweb',
        user = os.getenv('user'),
        password = os.getenv('password')
    )
    return conn

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# 首頁取得景點資訊
@app.route('/api/attractions')
def api_attractions():
	keyword = request.args.get('keyword', '')
	try:
		page = int(request.args.get('page', 0))
		conn = connect_to_db()
	except ValueError:
		return jsonify({'error': True, 'message': '頁數應為數字'}), 400
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	raw_data = []
	offset_num = page * 12
	cursor = conn.cursor()
	if keyword:
		cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id WHERE mrt.station=%s or sight.name LIKE %s GROUP BY sight.id LIMIT 13 OFFSET %s;', (keyword,'%'+keyword+'%', offset_num))
	else:
		cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id GROUP BY sight.id LIMIT 13 OFFSET %s;', (offset_num,))
	record = cursor.fetchall()
	cursor.close()
	conn.close()
	next_page = page + 1 if len(record) == 13 else None
	loop_len = 12 if len(record) >= 12 else len(record)
	for i in range(loop_len):
			tmp_dic = {}
			tmp_dic['id'] = record[i][0]
			tmp_dic['name'] = record[i][1]
			tmp_dic['category'] = record[i][9]
			tmp_dic['description'] = record[i][3]
			tmp_dic['address'] = record[i][4]
			tmp_dic['transport'] = record[i][5]
			tmp_dic['mrt'] = None if record[i][10]=='None' else record[i][10]
			tmp_dic['lat'] = record[i][7]
			tmp_dic['lng'] = record[i][8]
			tmp_dic['images'] = record[i][11].split(',')
			raw_data.append(tmp_dic)
	return jsonify({'nextPage': next_page, 'data': raw_data})

# 取得特定id的景點資訊
@app.route('/api/attraction/<attractionId>')
def api_attraction_id(attractionId):
	try:
		attractionId = int(attractionId)
		conn = connect_to_db()
	except ValueError:
		return jsonify({'error': True, 'message': '景點編號應為數字'}), 400
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id WHERE sight.id = %s GROUP BY sight.id', (attractionId,))
	record = cursor.fetchone()
	cursor.close()
	conn.close()
	if record == None:
		return jsonify({'error': True, 'message': '查無此景點編號'}), 400
	else:
		response_data = {'data': {}}
		response_data['data']['id'] = record[0]
		response_data['data']['name'] = record[1]
		response_data['data']['category'] = record[9]
		response_data['data']['description'] = record[3]
		response_data['data']['address'] = record[4]
		response_data['data']['transport'] = record[5]
		response_data['data']['mrt'] = record[10]
		response_data['data']['lat'] = record[7]
		response_data['data']['lng'] = record[8]
		response_data['data']['images'] = record[11].split(',')
		return jsonify(response_data)

# 取得捷運站列表
@app.route('/api/mrts')
def api_mrts():
	try:
		conn = connect_to_db()
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT mrt.station FROM mrt INNER JOIN sight ON mrt.id = sight.mrt_id GROUP BY mrt_id ORDER BY COUNT(sight.mrt_id) DESC;')
	record = cursor.fetchall()
	record = [item[0] for item in record]
	return jsonify({'data': record})

# 註冊會員 POST
@app.route('/api/user', methods = ['POST'])
def signup():
	data = request.get_json()
	name = data.get('name')
	email = data.get('email')
	password = data.get('password')
	signup_data = (name, email, password)
	try:
		conn = connect_to_db()
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM member WHERE email=%s;', (email,))
	email_has_been_used = cursor.fetchone()
	if email_has_been_used:
		cursor.close()
		conn.close()
		return jsonify({'error': True, 'message': 'Email已經註冊帳戶'}), 400
	cursor.execute('INSERT INTO member(name, email, password) VALUES(%s, %s, %s);', signup_data)
	conn.commit()
	cursor.close()
	conn.close()
	return jsonify({'ok': True})

#  驗證會員 GET / 登入會員 PUT
@app.route(('/api/user/auth'), methods = ['GET', 'PUT'])
def signin():
	if request.method == 'GET':
		load_dotenv()
		secret_key = os.getenv('key')
		auth_header = request.headers.get('Authorization')
		if auth_header:
			try:
				token = auth_header.split(' ')[1]
				payload = jwt.decode(token, secret_key, algorithms=['HS256'])
				return jsonify({'data':payload})
			except:
				return jsonify({'data': None})
	elif request.method == 'PUT':
		data = request.get_json()
		email = data.get('email')
		password = data.get('password')
		signin_data = (email, password)
		try:
			conn = connect_to_db()
		except:
			return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
		cursor = conn.cursor()
		cursor.execute('SELECT id, name, email FROM member WHERE email=%s AND password=%s;',(signin_data))
		member_info = cursor.fetchone()
		cursor.close()
		conn.close()
		if member_info:
			load_dotenv()
			secret_key = os.getenv('key')
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
				'id': member_info[0],
				'name': member_info[1],
				'email': member_info[2]
			}
			token = jwt.encode(payload, secret_key, algorithm="HS256")
			return jsonify({'token': token})
		else:
			return jsonify({'error': True, 'message': 'Email或密碼輸入錯誤'}), 400

# 預定行程
@app.route('/api/booking', methods = ['GET', 'POST', 'DELETE'])
def api_booking():
	load_dotenv()
	secret_key = os.getenv('key')
	auth_header = request.headers.get('Authorization')
	try:
		token = auth_header.split(' ')[1]
		payload = jwt.decode(token, secret_key, algorithms=['HS256'])
	except:
		return jsonify({'error': True, 'message': '會員未登入'}), 403
	else:
		member_id = payload['id']
	try:
		conn = connect_to_db()
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	if request.method == 'GET':
		cursor.execute('SELECT booking.*, sight.name, sight.address, image.url FROM booking INNER JOIN sight ON booking.sight_id=sight.id INNER JOIN image ON booking.sight_id=image.sight_id WHERE booking.member_id=%s ORDER BY image.id ASC LIMIT 1;', (member_id,))
		record = cursor.fetchone()
		cursor.close()
		conn.close()
		if record:
			attraction_data = {
				'id': record[2],
				'name': record[6],
				'address': record[7],
				'image': record[8]
			}
			data = {
				'attraction': attraction_data,
				'date': record[3],
				'time': record[4],
				'price': record[5]
			}
			return jsonify({'data': data})
		else:
			return jsonify({'data': None})
	elif request.method == 'POST':
		data = request.get_json()
		attraction_id = data.get('attractionId')
		date = data.get('date')
		time = data.get('time')
		price = data.get('price')
		booking_data = (member_id, attraction_id, date, time, price)
		success = True
		try:
			cursor.execute('INSERT INTO booking(member_id, sight_id, date, time, price) VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE sight_id = VALUES(sight_id), date = VALUES(date), time = VALUES(time), price = VALUES(price);', booking_data)
			conn.commit()
			return jsonify({'ok': True})
		except:
			success = False
		finally:
			cursor.close()
			conn.close()
		if success == False:
			return jsonify({'error': True, 'message': '輸入不正確'}), 400
	elif request.method == 'DELETE':
		cursor.execute('DELETE FROM booking WHERE member_id=%s', (member_id,))
		conn.commit()
		cursor.close()
		conn.close()
		return jsonify({'ok': True})

app.run(host="0.0.0.0", port=3000)