import time
import re

class OrderDataProcessor:

    @staticmethod
    def _generate_order_id(user_id):
        time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        order_id = str(user_id).zfill(3) + '-' + time_stamp
        return order_id
    
    @staticmethod
    def process_order_data(user_id, raw_data):
        order_id = OrderDataProcessor._generate_order_id(user_id)
        order_data = (
            order_id,
            user_id,
            raw_data['contact']['name'],
            raw_data['contact']['email'],
            raw_data['contact']['phone'],
            raw_data['order']['trip']['attraction']['id'],
            raw_data['order']['trip']['date'],
            raw_data['order']['trip']['time'],
            raw_data['order']['price'],
            False
        )
        return order_data
    
    @staticmethod
    def process_tappay_response_data(order_data, tappay_response):
        order_id = order_data[0]
        payment_result = {
            'number': order_id,
            'payment': {
                'status': tappay_response['status'],
                'message': tappay_response['msg']
            }
        }
        return {'data': payment_result}
    
class ContactDataChecker:

    def _is_email_correct(email):
        email_pattern = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
        if re.match(email_pattern, email):
            return True
        else:
            return False
        
    def _is_phone_correct(phone):
        phone_pattern = r'^09\d{8}$'
        if re.match(phone_pattern, phone):
            return True
        else:
            return False
        
    def is_contact_data_correct(data):
        check_email = ContactDataChecker._is_email_correct(data['email'])
        check_phone = ContactDataChecker._is_phone_correct(data['phone'])
        if check_email and check_phone:
            return {'ok': True}, 200
        else:
            return {'error': True, 'message': 'incorrect contact information'}, 400
