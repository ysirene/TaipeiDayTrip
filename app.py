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
	
@app.route('/api/mrts')
def mrts():
	try:
		conn = connect_to_db()
	except:
		return jsonify({'error': True, 'message': '無法連線到資料庫'}), 500
	cursor = conn.cursor()
	cursor.execute('SELECT mrt.station FROM mrt INNER JOIN sight ON mrt.id = sight.mrt_id GROUP BY mrt_id ORDER BY COUNT(sight.mrt_id) DESC;')
	record = cursor.fetchall()
	record = [item[0] for item in record]
	return jsonify({'data': record})

	
app.run(host="0.0.0.0", port=3000)