import sqlite3 as lite


class DbManager:
	"""Initialize a db connection with sqlite3"""
	def __init__(self):
		db_name = "amity.db"
		self.connection = lite.connect(db_name)
		self.cursor = self.connection.cursor()
		self.migrations()

	def migrations(self):
		""" Creates tables in case they do not exist """
		with self.connection:
			self.cursor.executescript("""
				CREATE TABLE IF NOT EXISTS rooms (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT UNIQUE,
				type CHAR(1)
				);
				CREATE TABLE IF NOT EXISTS fellows (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				accomodation TEXT,
				room_id INTEGER
				);
				CREATE TABLE IF NOT EXISTS staff (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				room_id INTEGER
				);
				""")

	def execute_many_querries(self, query_string, data):
		""" To querry multiple commands without using for loops """
		try:
			with self.connection:
				self.cursor.executemany(query_string, data)
				return True
		except lite.Error as er:
			print ('er: %s' % er)
			return False

	def insert(self, query_string):
		"""
		run various sqllite querries and returns the id of last item
		Arguments:
				query_string args> sql command to run

		"""
		try:
			with self.connection:
				self.cursor.execute(query_string)
				return self.cursor.lastrowid
		except lite.IntegrityError:
			return False

	def update(self, query_string):
		"""
		Method to update records
		Arguments:
				query_string string> sql command to run

		"""
		# import ipdb
		# ipdb.set_trace()

		try:
			with self.connection:
				self.cursor.execute(query_string)
				return self.cursor.lastrowid
		except lite.Error as er:
			print ('er: %s' % er)
			return False

	def select_all(self, query_string):
		"""
		Method to select data from sqlite

		Arguments:
				query_string sql command to execute.

		"""
		try:
			with self.connection:
				self.cursor.execute(query_string)
				return self.cursor.fetchall()
		except:
			return False

	def select_one(self, query_string):
		"""
		Method to select one record from data

		Arguments:
				query_string sql command to run

		"""
		try:
			with self.connection:
				# import ipdb
				# ipdb.set_trace()
				self.cursor.execute(query_string)
				return self.cursor.fetchall()
		except:
			return False
















	 