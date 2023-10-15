from flask import Blueprint, jsonify, request

from views.user import TokenDataProcessor
from views.booking import BookingDataProcessor
from views.booking import BookingDataChecker
from models.booking import BookingDataFetcher

booking = Blueprint('booking', __name__)

# 取得預定行程 GET / 新增預定行程 POST / 刪除預定行程 DELETE
@booking.route('/api/booking', methods = ['GET', 'POST', 'DELETE'])
def api_booking():
    auth_header = request.headers.get('Authorization')
    payload = TokenDataProcessor.decode_token(auth_header)
    user_data_response, status_code = TokenDataProcessor.is_payload(payload)
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

        check_input_data_response, status_code = BookingDataChecker.check_input_data(date, time, price)
        if status_code != 200:
            return jsonify(check_input_data_response), status_code

        new_booking_data = (user_id, attraction_id, date, time, price)
        response, status_code = BookingDataFetcher.add_booking_data(new_booking_data)
        return jsonify(response), status_code
    
    elif request.method == 'DELETE':
        response, status_code = BookingDataFetcher.delete_booking_data(user_id)
        return jsonify(response), status_code