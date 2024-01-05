import os

import mysql.connector
from dotenv import load_dotenv

class DB_Connector:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(DB_Connector, cls).__new__(cls)
			cls._instance.init_connection_pool()
			return cls._instance

	def init_connection_pool(self):
		load_dotenv()
		db_config = {
			'host': 'localhost',
			'database': 'tripweb',
			'user': os.getenv('user'),
			'password': os.getenv('password')
		}
		self.cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
			pool_name = 'conn_pool',
			pool_size = 3,
			**db_config
		)

	def get_connection_and_cursor(self):
		conn = self.cnx_pool.get_connection()
		cursor = conn.cursor()
		return conn, cursor

	def release_connection_and_cursor(self, conn, cursor):
		cursor.close()
		conn.close()