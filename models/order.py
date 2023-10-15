import os
import requests

from flask import current_app
from dotenv import load_dotenv

class OrderDataFetcher:

    def _request_payment_for_order(partner_key, merchant_id, prime, order_data):
        request_headers = {
            'Content-Type': 'application/json',
            'x-api-key': partner_key
        }
        request_body = {
            'prime': prime,
            'partner_key': partner_key,
            'merchant_id': merchant_id,
            'details':'台北一日遊行程',
            'amount': order_data[8],
            'order_number': order_data[0],
            'cardholder': {
                'phone_number': order_data[4],
                'name': order_data[2],
                'email': order_data[3],
            },
        }
        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        r = requests.post(url, headers = request_headers, json = request_body, timeout = 30)
        return r.json()

    def add_order(order_data, prime):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        
        try:
            cursor.execute('INSERT INTO orders(id, member_id, contact_name, contact_email, contact_phone, sight_id, date, time, price, payment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', order_data)
            conn.commit()
        except:
            cnx_pool.release_connection_and_cursor(conn, cursor)
            return {'error': True, 'message': 'incorrect order information'}, 400
        
        load_dotenv('../.env')
        partner_key = os.getenv('partner_key')
        merchant_id = os.getenv('merchant_id')
        tappay_response = OrderDataFetcher._request_payment_for_order(partner_key, merchant_id, prime, order_data)
        if tappay_response['status'] == 0:
            order_id = order_data[0]
            user_id = order_data[1]
            cursor.execute('UPDATE orders SET payment=1 WHERE id=%s', (order_id,))
            conn.commit()
            cursor.execute('DELETE FROM booking WHERE member_id=%s', (user_id,))
            conn.commit()
            cnx_pool.release_connection_and_cursor(conn, cursor)
        return tappay_response, 200