import time

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