from flask import Blueprint, jsonify, request

from views.user import UserDataProcessor
from views.booking import BookingDataProcessor
from models.booking import BookingDataFetcher

booking = Blueprint('booking', __name__)

# 取得預定行程 GET
@booking.route('/api/booking', methods = ['GET', 'POST', 'DELETE'])
def api_booking():
    auth_header = request.headers.get('Authorization')
    payload = UserDataProcessor.decode_token(auth_header)
    user_data_response, status_code = UserDataProcessor.is_payload(payload)
    if status_code != 200:
        return jsonify(user_data_response), status_code
    user_id = user_data_response['id']
	
    if request.method == 'GET':
        booking_data_response, status_code = BookingDataFetcher.get_booking_data(user_id)
        if status_code != 200:
            return jsonify(booking_data_response), status_code
        processed_data = BookingDataProcessor.process_booking_data(booking_data_response)
        return jsonify(processed_data)
	
    elif request.method == 'POST':
        data = request.get_json()
        attraction_id = data.get('attractionId')
        date = data.get('date')
        time = data.get('time')
        price = data.get('price')
        new_booking_data = (user_id, attraction_id, date, time, price)
        response, status_code = BookingDataFetcher.add_booking_data(new_booking_data)
        return jsonify(response), status_code
    
    elif request.method == 'DELETE':
        response, status_code = BookingDataFetcher.delete_booking_data(user_id)
        return jsonify(response), status_code
         
		

	


# @booking.route('/api/booking', methods = ['GET', 'POST', 'DELETE'])
# def api_booking():
	# secret_key = os.getenv('secret_key')
	# auth_header = request.headers.get('Authorization')
	# try:
	# 	token = auth_header.split(' ')[1]
	# 	payload = jwt.decode(token, secret_key, algorithms=['HS256'])
	# except:
	# 	return jsonify({'error': True, 'message': 'not logged in'}), 403
	# else:
	# 	member_id = payload['id']
	# try:
	# 	conn, cursor = DB_Connector.get_connection_and_cursor(cnx_pool)
	# except:
	# 	return jsonify({'error': True, 'message': 'cannot connect to database'}), 500
	# if request.method == 'GET':
		# cursor.execute('SELECT booking.*, sight.name, sight.address, image.url FROM booking INNER JOIN sight ON booking.sight_id=sight.id INNER JOIN image ON booking.sight_id=image.sight_id WHERE booking.member_id=%s ORDER BY image.id ASC LIMIT 1;', (member_id,))
		# record = cursor.fetchone()
		# DB_Connector.release_connection_and_cursor(conn, cursor)
		# if record:
		# 	attraction_data = {
		# 		'id': record[2],
		# 		'name': record[6],
		# 		'address': record[7],
		# 		'image': record[8]
		# 	}
		# 	data = {
		# 		'attraction': attraction_data,
		# 		'date': record[3],
		# 		'time': record[4],
		# 		'price': record[5]
		# 	}
		# 	return jsonify({'data': data})
		# else:
		# 	return jsonify({'data': None})
	# elif request.method == 'POST':
		# data = request.get_json()
		# attraction_id = data.get('attractionId')
		# date = data.get('date')
		# time = data.get('time')
		# price = data.get('price')
		# booking_data = (member_id, attraction_id, date, time, price)
		# try:
		# 	cursor.execute('INSERT INTO booking(member_id, sight_id, date, time, price) VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE sight_id = VALUES(sight_id), date = VALUES(date), time = VALUES(time), price = VALUES(price);', booking_data)
		# 	conn.commit()
		# 	DB_Connector.release_connection_and_cursor(conn, cursor)
		# 	return jsonify({'ok': True})
		# except:
		# 	DB_Connector.release_connection_and_cursor(conn, cursor)
		# 	return jsonify({'error': True, 'message': 'incorrect input'}), 400
	# elif request.method == 'DELETE':
	# 	cursor.execute('DELETE FROM booking WHERE member_id=%s', (member_id,))
	# 	conn.commit()
	# 	DB_Connector.release_connection_and_cursor(conn, cursor)
	# 	return jsonify({'ok': True})