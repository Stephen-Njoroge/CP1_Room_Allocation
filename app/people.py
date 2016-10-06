class Person(object):
	"""Defines Persons and handles room allocation methods for Fellows and Staff.
	"""
	def __init__(self):
		""" Initialize the database """
		self.db = DbManager()

	def register_name(self, first_name, last_name):
		""" Helps to return first letter capitalized names and also enables doc-opt to 
		receive:
		Arguments:
				first_name (str)
				last_name (str)
		"""
		name = first_name + " " + last_name
		self.name = name.title()

class Staff(Person):
	"""Handles the expected functionalities of a staff member"""
	def __init__(self):
		""" Initialize database """
		self.person = Person()

	def add_staff(self, args):
		"""To add a new staff member to the database and allocate them an office

		Arguments:
				args (dict) The first and last name of a staff member
		"""
		self.person.register_name(args['<first_name>'], args['<last_name>'])
		pass
	def relocate(self, args):
		"""
		Method to relocate a member of staff to a new office space

		Arguments:
				args (dict) contains the persons id and room to move to

		"""
		pass

class Fellow(Person):
	"""Defines the expected functionalities of a fellow""" 
	def __init__(self):
		"""initialize the database"""
		self.person = Person()

	def add_fellow(self, args):
		"""Method to add a fellow to the database and allocate them an office and accomodation
		Arguments:
				args (dict) The first and last name of a Fellow and Y for wants accomodation
		"""
		self.person.register_name(args['<first_name>'], args['<last_name>'])
		self.accomodation = 'Y'
		pass

	def relocate(self, args):
		"""
		Relocate a fellow to a new office or living space

		Arguments:
				args (dict) Fellows id and room to relocate to.

		"""
		pass
