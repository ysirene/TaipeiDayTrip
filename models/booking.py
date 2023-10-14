from flask import current_app

class BookingDataFetcher:

    @staticmethod
    def get_booking_data(user_id):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('SELECT booking.*, sight.name, sight.address, image.url FROM booking INNER JOIN sight ON booking.sight_id=sight.id INNER JOIN image ON booking.sight_id=image.sight_id WHERE booking.member_id=%s ORDER BY image.id ASC LIMIT 1;', (user_id,))
        data = cursor.fetchone()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return data, 200
    
    @staticmethod
    def add_booking_data(new_booking_data):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        try:
            cursor.execute('INSERT INTO booking(member_id, sight_id, date, time, price) VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE sight_id = VALUES(sight_id), date = VALUES(date), time = VALUES(time), price = VALUES(price);', new_booking_data)
            conn.commit()
            cnx_pool.release_connection_and_cursor(conn, cursor)
            return {'ok': True}, 200
        except:
            cnx_pool.release_connection_and_cursor(conn, cursor)
            return {'error': True, 'message': 'incorrect input'}, 400
        
    @staticmethod
    def delete_booking_data(user_id):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('DELETE FROM booking WHERE member_id=%s', (user_id,))
        conn.commit()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return {'ok': True}, 200