from flask import Blueprint, jsonify, request

from views.user import UserDataProcessor
from views.order import OrderDataProcessor
from models.order import OrderDataFetcher

order = Blueprint('order', __name__)

# 訂單付款
@order.route('/api/orders', methods = ['POST'])
def api_order():
    auth_header = request.headers.get('Authorization')
    payload = UserDataProcessor.decode_token(auth_header)
    user_data_response, status_code = UserDataProcessor.is_payload(payload)
    if status_code != 200:
        return jsonify(user_data_response), status_code
	
    if request.method == 'POST':
        user_id = user_data_response['id']
        data = request.get_json()
        order_data = OrderDataProcessor.process_order_data(user_id, data)
        prime = data['prime']
        response, status_code = OrderDataFetcher.add_order(order_data, prime)
        if status_code != 200:
            return jsonify(response), status_code
        else:
            payment_result = OrderDataProcessor.process_tappay_response_data(order_data, response)
            return jsonify(payment_result)

	# try:
	# 	conn, cursor = DB_Connector.get_connection_and_cursor(cnx_pool)
	# except:
	# 	return jsonify({'error': True, 'message': 'cannot connect to database'}), 500
	# data = request.get_json()
	# order_id = generate_order_id(member_id)
	# order_data = (
	# 	order_id,
	# 	member_id,
	# 	data['contact']['name'],
	# 	data['contact']['email'],
	# 	data['contact']['phone'],
	# 	data['order']['trip']['attraction']['id'],
	# 	data['order']['trip']['date'],
	# 	data['order']['trip']['time'],
	# 	data['order']['price'],
	# 	False
	# )
	# try:
	# 	cursor.execute('INSERT INTO orders(id, member_id, contact_name, contact_email, contact_phone, sight_id, date, time, price, payment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', order_data)
	# 	conn.commit()
	# except:
	# 	DB_Connector.release_connection_and_cursor(conn, cursor)
	# 	return jsonify({'error': True, 'message': 'Incorrect order information'})
	# prime = data['prime']
	# partner_key = os.getenv('partner_key')
	# merchant_id = os.getenv('merchant_id')
	# tappay_response = request_payment_for_order(partner_key, merchant_id, prime, order_data)
	# if tappay_response['status'] == 0:
	# 	cursor.execute('UPDATE orders SET payment=1 WHERE id=%s', (order_id,))
	# 	conn.commit()
	# 	cursor.execute('DELETE FROM booking WHERE member_id=%s', (member_id,))
	# 	conn.commit()
	# 	DB_Connector.release_connection_and_cursor(conn, cursor)
	# payment_result = {
	# 	'number': order_id,
	# 	'payment': {
	# 		'status': tappay_response['status'],
	# 		'message': tappay_response['msg']
	# 	}
	# }
	# return jsonify({'data': payment_result})