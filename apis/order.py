from flask import Blueprint, jsonify, request

from views.user import TokenDataProcessor
from views.order import OrderDataProcessor
from views.order import ContactDataChecker
from models.order import OrderDataFetcher

order = Blueprint('order', __name__)

# 訂單付款
@order.route('/api/orders', methods = ['POST'])
def api_order():
    auth_header = request.headers.get('Authorization')
    payload = TokenDataProcessor.decode_token(auth_header)
    user_data_response, status_code = TokenDataProcessor.is_payload(payload)
    if status_code != 200:
        return jsonify(user_data_response), status_code
    user_id = user_data_response['id']
	
    if request.method == 'POST':    
        data = request.get_json()

        is_contact_data_correct_response, status_code = ContactDataChecker.is_contact_data_correct(data['contact'])
        if status_code != 200:
            return jsonify(is_contact_data_correct_response), status_code
        
        order_data = OrderDataProcessor.process_order_data(user_id, data)
        prime = data['prime']
        response, status_code = OrderDataFetcher.add_order(order_data, prime)
        if status_code != 200:
            return jsonify(response), status_code
        else:
            payment_result = OrderDataProcessor.process_tappay_response_data(order_data, response)
            return jsonify(payment_result)