from flask import current_app

class MrtDataFetcher:

    def get_mrt_data():
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('SELECT mrt.station FROM mrt INNER JOIN sight ON mrt.id = sight.mrt_id GROUP BY mrt_id ORDER BY COUNT(sight.mrt_id) DESC;')
        data = cursor.fetchall()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return data, 200
