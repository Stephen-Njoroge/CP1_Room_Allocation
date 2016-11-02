"""People Classes"""
import random
from db.dbManager import DbManager
from tkinter import filedialog as fd
from .rooms import Room, LivingRoom, OfficeRoom
from shutil import copyfile

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
	def all_unallocated(self, args):
		"""
		prints all unallocated employees

		"""
		unallocated_fellows = Fellow().unallocated_employees("fellow")
		unallocated_staff = Staff().unallocated_employees("staff")

		output = ''
		output += '*' * 30 + "\nSTAFF\n" + '*' * 30 + "\n"
		if unallocated_staff and len(unallocated_staff) != 0:
			output += "\n".join([str(x[1]) for x in unallocated_staff])
		else:
			output += 'Currently there are no unallocated members of staff'

		output += '\n\n' + '*' * 30 + "\nFELLOWS\n" + '*' * 30 + "\n"
		if unallocated_fellows and len(unallocated_fellows) != 0:
			output += "\n".join([str(x[1]) + '\t[' +
								 str(x[2]) + ']' for x in unallocated_fellows])
		else:
			output += 'There are no unallocated fellows currently'

		print(output)
		if args['--o']:
			with open(args['--o'], 'wt') as file:
				file.write(output)
				print("Check all unallocated in {}"
					.format(args['--o']))
	def allocations_from_file(self, args):
		"""
		Allocate rooms using a file

		"""
		file = fd.askopenfile(
			mode='rt', title='Import the list of people to allocate rooms.')

		fellows = []
		staff = []
		with open(file.name, 'r') as f:
			people = f.readlines()
			for person in people:
				person = person.split()
				person_type = 'F' if person[2] == 'FELLOW' else 'S'

				if person_type == 'F':
					try:
						fellow = {}
						fellow['<first_name>'] = person[0]
						fellow['<last_name>'] = person[1]
						fellow['--a'] = person[3]
						fellows.append(fellow)
					except:
						raise ValueError("Invalid data in file")

				else:
					staff_member = {}
					staff_member['<first_name>'] = person[0]
					staff_member['<last_name>'] = person[1]
					staff.append(staff_member)

			for x in range(len(fellows)-1):
				print(Fellow().add_fellow(fellows[x]))

			for j in range(len(staff)-1):
				print(Staff().add_staff(staff[j]))

	def unallocated_employees(self, person_type):
		"""
		Process a list of unallocated employees
		Arguments:
				person_type If fellow or staff
		"""
		if person_type == "fellow":
			unallocated = self.person.db.select_all("""SELECT * FROM fellows
				WHERE room_id is NULL or room_id = ''""")
		elif person_type == "staff":
			unallocated = self.person.db.select_all("""SELECT * FROM staff
			WHERE room_id is NULL or room_id = ''""")
		if unallocated:
			return unallocated

	def load_database(self):
		'''To load all the data in the database'''
		rooms = self.db.select_all("""SELECT * FROM rooms""")
		staff = self.db.select_all("""SELECT * FROM staff""")
		fellows = self.db.select_all("""SELECT * FROM fellows""")

		print('rooms \n {}'.format(rooms))
		print('staff \n {}'.format(staff))
		print('fellows \n {}'.format(fellows))

	def save_database(self, args):
		destination_path = ('/Users/steve254/Documents/amity/CP1_Room_Allocation')
		filename = args['<filename>']
		if not filename:
			filename = 'Amity.db'
		copyfile(destination_path + '/amityrecords.db', destination_path + '/' + '{}'.format(filename))




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
		
		office_spaces = Room().vacancies("office")
		if len(office_spaces) != 0:
			office_space = random.choice(office_spaces)
			new_staff = """INSERT INTO staff(name, room_id)
			VALUES ('{}', {})""" .format(self.person.name, office_space[0])

		else:
			new_staff = """INSERT INTO staff(name, room_id)
			VALUES ('{}', NULL)""" .format(self.person.name)

		staff_id = self.person.db.insert(new_staff)

		if staff_id:
			print("{} Added! at Staff ID {}"
				.format(self.person.name, staff_id))

			if len(office_spaces) != 0:
				print("{} has been allocated {}."
					.format(self.person.name, office_space[1]))
				return True

			raise ValueError(
				"All rooms are full! Sorry {}" .format(
					self.person.name))

	def relocate(self, args):
		"""
		Method to relocate a member of staff to a new office space

		Arguments:
				args (dict) contains the persons id and room to move to

		"""
		staff_id = int(args['<person_identifier>'])
		staff = self.person.db.select_one(
			"SELECT * FROM staff WHERE id = {}" .format(staff_id))
		# import ipdb
		# ipdb.set_trace()
		
		if staff:
			if staff[0][2]:
				current_room = self.person.db.select_one(
					"""SELECT * FROM rooms 
					WHERE id = {} AND type='O'""" .format(staff[0][2]))
			else:
				current_room = [(None, 'has no office space')]

			new_room_name = args['<new_room_name>']
			# import ipdb
			# ipdb.set_trace()

			if current_room[0][1] != new_room_name:
				office = OfficeRoom()
				new_room = office.exists("O", new_room_name)
				# import ipdb
				# ipdb.set_trace()

				if new_room:
					room_occupants = office.occupants("office", new_room[0][0])
					if len(room_occupants) < office.room_capacity:
						office.allocate_room("staff", staff_id,
												new_room[0][0])
						print("{} transfered to {}!".format(
								staff[0][1], new_room_name))
					else:
						raise ValueError(
							"No vacant space in {}." .format(new_room_name))
				else:
					raise ValueError(
						"An office with that name does not exist.")
			else:
				raise ValueError(
					"{} already belongs in {}." .format(staff[0][1], new_room_name))
		else:
			raise ValueError(
				"{} is not a registered staff" .format(staff_id))

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
		self.accomodation = 'Y' if args['--a'] is not None\
							and args['--a'].lower() == 'y' else 'N'

		fellow_id = self.person.db.insert(
			"""INSERT INTO fellows (name, accomodation)
			VALUES ('{}', '{}');""".format(
				self.person.name, self.accomodation))

		if fellow_id:
			print("{} added with id {}"
				.format(self.person.name, fellow_id))
			if self.accomodation == 'Y':
				self.accomodate_fellow(fellow_id)
				print('Fellow succesfully Acomodated!\n')
			else:
				return 'Fellow added with no accomodation!'
	def accomodate_fellow(self, fellow_id):
		"""Assign a new fellow a living space"""

		vacant_living_spaces = Room().vacancies("living")

		if len(vacant_living_spaces) != 0:
			living_space = random.choice(vacant_living_spaces)
			query_db = """UPDATE fellows
			SET room_id = {} WHERE id = {}""" .format(
				living_space[0], fellow_id)

			if self.person.db.update(query_db):
				print("{} assigned {}".format(
					self.person.name, living_space[1]))
				return True
		else:
			raise ValueError(
				"All rooms are full. Say sorry to {}" .format(
					self.person.name))

	def relocate(self, args):
		"""Relocate a fellow

		 Arguments:
				args (dict) User's input
		"""
		fellow_id = int(args['<person_identifier>'])
		fellow = self.person.db.select_one(
			"SELECT * FROM fellows WHERE id = {}".format (fellow_id))
		
		if fellow:
			if fellow[0][2] == 'N':
				accommodate = input(
					"""{} Does not need accomodation. 
					Do you still want to accomodate the fellow?[y/n]""" .format(fellow[0][1]))

				if accommodate.upper() == 'Y':
					return self.allocate_fellow(fellow[0][2], fellow_id, args)
				else:
					print("{} has not been allocated into any room." 
					.format(fellow[0][1]))
			else:
				return self.reallocate_fellow(fellow, fellow_id, args)
		else:
			raise ValueError(
				"No fellow by the fellow id {}" .format(fellow_id))

	def reallocate_fellow(self, fellow, fellow_id, args):
		"""
		Relocate a fellow to a new office or living space

		Arguments:
				args (dict) users request

		Returns:
			List    Record of a living space

		"""
		if fellow:
			current_room = self.person.db.select_one(
				"""SELECT * FROM rooms
				WHERE id = {}
				AND type='L'""" .format(fellow[0][3]))
			current_room = current_room[0][1]
		else:
			current_room = 'does not have a room'		

		new_room_name = args['<new_room_name>']
		
		if current_room != new_room_name:
			return self.allocate_fellow(fellow, fellow_id, args)
		else:
			raise ValueError(
			"{} already belongs in {}" .format(fellow[0][1], new_room_name))

	def allocate_fellow(self, fellow, fellow_id, args):
		"""To allocate a fellow to a new room

		 Arguments:
				fellow  (List)  Fellows detail
				fellow_id (Int) Fellow's id
				args (dict)     User's request
		"""
		new_room_name = args['<new_room_name>']
		living = LivingRoom()
		new_room = living.exists("L", new_room_name)
		
		if new_room:
			room_occupants = living.occupants("living", new_room[0][0])
			if len(room_occupants) < LivingRoom.room_capacity:
				if living.allocate_room("fellow", fellow_id, new_room[0][0]):
					return "{} assigned to {}" .format(
						fellow[1], new_room_name)
			else:
				raise ValueError("{} has no vacant space." .format(new_room_name))
		else:
			raise ValueError("A room with that name does not exist.")



