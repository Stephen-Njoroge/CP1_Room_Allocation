class Room(object):
	"""
	Handles room functionalities that are common to
	both living spaces and office rooms.

	"""
	def __init__(self):
		"""Initialize the database"""
		self.db = DbManager()

	def create_room(self, args):
		"""
		A method to create rooms in the database

		Arguments:
		args (dict) name of the room and the type of room

		"""
		pass
	def allocate_room(self, person_type, person_id, room_id):
		"""
		Method to allocate rooms to People 

		Arguments:
				person_type fellow or staff
				person_id id of the fellow or staff 

		"""
		pass

	def show_all_allocations(self,args):
		"""
		Method to print all room allocations

		Arguments: 
				args a file name to print out room allocations
		"""
		pass

	def show_particular_room_allocation():
		"""
		method to show allocations for a particular room

		Arguments:
			args (dict) The room name and a filename to print the details

		"""

		pass
class OfficeSpace(Room):
	"""
	Specifies office space particulars

	"""
	room_space = 6

	def __init__(self):
		"""initialize the database"""
		self.rooms = Room()
		self.db = DbManager

class LivingSpace(Room):
	"""
	Specifies living space particulars

	"""

	def __init__(self):
		"""initialize the database"""
		self.rooms = Room()
		self.db = DbManager



