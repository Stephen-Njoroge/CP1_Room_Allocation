from app.rooms import Room
from app.people import Fellow, Staff
from db.dbManager import DbManager
import os

class MockData:
	"""Class to avail data for tests"""

	db_name = 'mock_db'

	def __init__(self):
		"""A test database """
		self.db = DbManager()
    def create_fellow(self, first_name, last_name, accomodation):
        arguments = {'<first_name>': first_name,
                    '<last_name>': last_name,
                     '--a': accomodation}
        fellow = Fellow()
        return fellow.add_fellow(arguments)
