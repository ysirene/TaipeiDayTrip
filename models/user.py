from flask import current_app

class UserDataFetcher:

    def signup(name, email, password):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('SELECT * FROM member WHERE email=%s;', (email,))
        email_has_been_used = cursor.fetchone()
        if email_has_been_used:
            cnx_pool.release_connection_and_cursor(conn, cursor)
            return {'error': True, 'message': 'email is already registered'}, 400
        cursor.execute('INSERT INTO member(name, email, password) VALUES(%s, %s, %s);', (name, email, password))
        conn.commit()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return {'ok': True}, 200

    def signin(email, password):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('SELECT id, name, email FROM member WHERE email=%s AND password=%s;',(email, password))
        user_info = cursor.fetchone()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return user_info, 200