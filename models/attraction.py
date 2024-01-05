from flask import current_app

class AttractionDataFetcher:
    
    def get_index_attractions(keyword, page):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        offset_num = page * 12
        if keyword:
            cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id WHERE mrt.station=%s or sight.name LIKE %s GROUP BY sight.id LIMIT 13 OFFSET %s;', (keyword,'%'+keyword+'%', offset_num))
        else:
            cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id GROUP BY sight.id LIMIT 13 OFFSET %s;', (offset_num,))
        data = cursor.fetchall()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        return data, 200
    
    def get_specific_attraction(attraction_id):
        try:
            cnx_pool = current_app.config['cnx_pool']
            conn, cursor = cnx_pool.get_connection_and_cursor()
        except:
            return {'error': True, 'message': 'cannot connect to database'}, 500
        cursor.execute('SELECT sight.*, category.cat, mrt.station, GROUP_CONCAT(DISTINCT image.url ORDER BY image.id ASC) FROM sight INNER JOIN mrt ON sight.mrt_id=mrt.id INNER JOIN category ON sight.category_id=category.id INNER JOIN image ON sight.id=image.sight_id WHERE sight.id = %s GROUP BY sight.id', (attraction_id,))
        data = cursor.fetchone()
        cnx_pool.release_connection_and_cursor(conn, cursor)
        if data == None:
            return {'error': True, 'message': 'attraction id not found'}, 400
        else:
            return data, 200
