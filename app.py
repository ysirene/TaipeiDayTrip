from flask import *
import mysql.connector
import os
from dotenv import load_dotenv

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

@app.route('/api/attractions')
def api_attractions():
	keyword = request.args.get('keyword', '')
	try:
		page = int(request.args.get('page', 0))
		conn = connect_to_db()
	except ValueError:
		return jsonify({'error': True, 'message': '頁數應為數字'}), 400
	except mysql.connector.ProgrammingError:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	raw_data = []
	cursor = conn.cursor()
	if keyword:
		cursor.execute('SELECT sight.* FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id WHERE mrt.station=%s or sight.name LIKE %s;', (keyword,'%'+keyword+'%'))
	else:
		cursor.execute('SELECT * FROM sight')
	record = cursor.fetchall()
	cursor.close()
	conn.close()
	for i in range(len(record)):
			tmp_dic = {}
			tmp_dic['id'] = record[i][0]
			tmp_dic['name'] = record[i][1]
			tmp_dic['category'] = record[i][2]
			tmp_dic['description'] = record[i][3]
			tmp_dic['address'] = record[i][4]
			tmp_dic['transport'] = record[i][5]
			tmp_dic['mrt'] = record[i][6]
			tmp_dic['lat'] = record[i][7]
			tmp_dic['lng'] = record[i][8]
			tmp_dic['images'] = record[i][9].split(',')
			raw_data.append(tmp_dic)
	total_pages = len(raw_data) // 12
	if page > total_pages:
		return jsonify({'nextPage': None, 'data': []})
	else:
		if page == total_pages:
			return jsonify({'nextPage': None, 'data': raw_data[12*page:]})
		else:
			return jsonify({'nextPage': page + 1, 'data': raw_data[12*page: 12*(page+1)+1]})

@app.route('/api/attraction/<attractionId>')
def api_attraction_id(attractionId):
	try:
		attractionId = int(attractionId)
		conn = connect_to_db()
	except ValueError:
		return jsonify({'error': True, 'message': '景點編號應為數字'}), 400
	except mysql.connector.ProgrammingError:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM sight WHERE id = %s', (attractionId,))
	record = cursor.fetchone()
	cursor.close()
	conn.close()
	if record == None:
		return jsonify({'error': True, 'message': '查無此景點編號'}), 400
	else:
		response_data = {'data': {}}
		response_data['data']['id'] = record[0]
		response_data['data']['name'] = record[1]
		response_data['data']['category'] = record[2]
		response_data['data']['description'] = record[3]
		response_data['data']['address'] = record[4]
		response_data['data']['transport'] = record[5]
		response_data['data']['mrt'] = record[6]
		response_data['data']['lat'] = record[7]
		response_data['data']['lng'] = record[8]
		response_data['data']['images'] = record[9].split(',')
		return jsonify(response_data)
	
@app.route('/api/mrts')
def mrts():
	try:
		conn = connect_to_db()
	except mysql.connector.ProgrammingError:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT mrt.station FROM mrt INNER JOIN sight ON mrt.id = sight.mrt_id GROUP BY mrt.station ORDER BY COUNT(sight.mrt_id) DESC')
	record = cursor.fetchall()
	record = [item[0] for item in record]
	return jsonify({'data': record})

	
app.run(host="0.0.0.0", port=3000)