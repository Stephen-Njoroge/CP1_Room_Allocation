from app.rooms import Room
from app.people import Fellow, Staff
from db.dbManager import DbManager
import os

class MockData(object):
    """Class to avail data for tests"""

    db_name = 'mock.db'

    def __init__(self):
        """Create a test database"""
        self.db = DbManager()

    def create_living_spaces(self, room_names):
        rooms = Room()
        arguments = {'<room_name>': room_names,
                     'living': True,
                     'office': False}

        return rooms.create_room(arguments)

    def create_office_spaces(self, room_name):
        rooms = Rooms()
        arguments = {'<room_name>': room_name,
                     'living': False,
                     'office': True}

        return rooms.create_rooms(arguments)

    def fetch_data(self, table_name, single_record=True):
        if single_record:
            return self.db.select_one("SELECT * FROM %s" % (table_name))
        else:
            return self.db.select_all("SELECT * FROM  %s" % (table_name))

    def create_fellow(self, first_name, last_name, accomodation):
        arguments = {'<first_name>': first_name,
                     '<last_name>': last_name,
                     '--a': accomodation}
        fellow = Fellow()
        return fellow.add_fellow(arguments)

    def create_staff(self, first_name, last_name):
        arguments = {'<first_name>': first_name,
                     '<last_name>': last_name}
        staff = Staff()
        return staff.add_staff(arguments)

    def clear_test_db(self):
        """Clear the test database"""
        if os.path.exists('mock.db'):
            os.remove('mock.db')


