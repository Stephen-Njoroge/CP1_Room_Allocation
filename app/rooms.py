"""Room Classes"""
from db.dbManager import DbManager
from itertools import groupby

class Room(object):
	"""
	Handles room functionalities that are common to
	both living spaces and office rooms.

	"""
	
	

	def __init__(self):
		"""database instance"""
		self.db = DbManager()

	def create_room(self, args):
		"""
		A method to create rooms in the database

		Arguments:
		args (dict) name of the room and the type of room

		"""
		room_type = 'L' if args['living'] else 'O'
		rooms_list = tuple((room, room_type) for room in args["<room_name>"])

		if self.db.execute_many_querries("""INSERT INTO rooms(name, type)
			VALUES(?, ?)""", rooms_list):
			return 'New room(s) created!'
		else:
			raise ValueError(
				'Duplicate alert!: A room with that name already exists.')


	def show_all_allocations(self, args):
		"""
		Method to print all room allocations

		Arguments: 
				args an optional file name to print out room allocations

		"""
		office_rooms = self.db.select_all(
			"""SELECT rooms.id, rooms.name, rooms.type, staff.name
			FROM rooms
			LEFT JOIN staff ON rooms.id = staff.room_id
			WHERE rooms.type = 'O'""")

		living_rooms = self.db.select_all(
			"""SELECT rooms.id, rooms.name, rooms.type, fellows.name
			FROM rooms
			LEFT JOIN fellows ON rooms.id = fellows.room_id
			WHERE rooms.type = 'L'""")

		office_rooms_allocations = {}
		living_rooms_allocations = {}

		for _, group in groupby(office_rooms, lambda x: x[0]):
			staff_allocated = list(group)
			room_name = str(staff_allocated[0][1])
			office_rooms_allocations[room_name] = []
			for staff in staff_allocated:
				office_rooms_allocations[room_name].append(staff[-1])
		for _, group in groupby(living_rooms, lambda x: x[0]):
			fellow_allocated = list(group)
			room_name = str(fellow_allocated[0][1])
			living_rooms_allocations[room_name] = []
			for fellow in fellow_allocated:
				living_rooms_allocations[room_name].append(fellow[-1])

		try:
			office_space = [len(", ".join(x)) for x in office_rooms_allocations.values()
							if x[0]]

			living_space = [len(", ".join(x)) for x in living_rooms_allocations.values()
							if x[0]]

			divisions = max(max(office_space),
							max(living_space),
							len('LIVING ROOMS'),
							len('OFFICE ROOMS'))
		except ValueError:
			divisions = 30

		output = ""
		output += '\n' + '*' * divisions + "\nOFFICE ROOMS\n" + '*' * divisions + "\n\n"
		if len(office_space) != 0:
			for name, occupants in office_rooms_allocations.items():
				if occupants[0]:
					room_members = ", ".join(occupants)
					output += name + "\n" + '-' * divisions + "\n" + room_members + "\n\n"
		else:
			output += ":) All office rooms are empty!"

		output += '\n' + '*' * divisions + "\nLIVING ROOMS\n" + '*' * divisions + "\n\n"
		if len(living_space) != 0:
			for name, occupants in living_rooms_allocations.items():
				if occupants[0]:
					room_members = ", ".join(occupants)
					output += name + "\n" + '-' * divisions + "\n" + room_members + "\n\n"
					# import ipdb
					# ipdb.set_trace()
		else:
			output += ":) All living spaces are empty!"

		print(output)
		if args["--o"]:
			with open(args['--o'], 'wt') as file:
				file.write(output)
				print("Check allocations in {0}" .format(args['--o']))

	def show_particular_room_allocation(self, args):
		"""
		method to show allocations for a particular room

		Arguments:
			args (dict) The room name and a filename to print the details

		"""
		room_name = args['<room_name>']
		office = self.exists("O", room_name)
		living = self.exists("L", room_name)

		if office:
			room_type = "OFFICE ROOM"
			occupancy = self.occupants("office", office[0][0])


		elif living:
			room_type = "LIVING ROOM"
			occupancy = self.occupants("living", living[0][0])
			# import ipdb
			# ipdb.set_trace()

		else:
			return "A room with such a name does not exist! Try again."



		occupy = ", ".join([str(x[1]) for x in occupancy])
		divisions = max([len(occupy), len(room_type)])

		output = '*' * divisions + "\n"
		output += room_name.upper() + " (" + room_type + ")\n"
		output += '*' * divisions + "\n"

		if len(occupy) == 0:
			output += "{} is Vacant." .format(room_name)
		else:
			output += occupy
		print(output)

		if args['--o']:
			with open(room_name + ".txt", 'wt') as file:
				file.write(output)
				print("{room_name} occupants saved in {file}"
					.format(room_name, room_name + ".txt"))
				
	def allocate_room(self, person_type, person_id, room_id):
		"""
		Method to allocate rooms to People 

		Arguments:
				person_type fellow or staff
				person_id id of the fellow or staff 
				room_id id of the room to allocate

		"""
		if person_type == "fellow":
			update_room = """UPDATE fellows SET room_id = {}, accomodation = 'Y' WHERE id = {};""".format(room_id, person_id)

		elif person_type == "staff":
			update_room = """UPDATE staff SET room_id = {} WHERE id = {}""".format(room_id, person_id)
			
		if self.db.update(update_room):
			return True

	

	def occupants(self, room_type, room_id):
		"""
		Method to show the occupants of a given rooom.
		Arguments:
				room_type The type of room
				room_id The unique room identifier
		"""
		if room_type == "living":
			room = self.exists("L", room_id)
			if room:
				return self.db.select_all(
					"""SELECT * FROM fellows
					WHERE room_id = {}""" .format(room[0][0]))
		elif room_type == "office":
			room = self.exists("O", room_id)
			if room:
				return self.db.select_all(
					"""SELECT * FROM staff
					WHERE room_id = {0}""" .format(room[0][0]))

	def vacancies(self, room_type):
		"""
		Method to check available space in a room
		Arguments:
				room_type Whether living or office.

		"""
		if room_type == "living":
			return self.db.select_all(
				"""SELECT rooms.id, rooms.name, rooms.type,
				COUNT(*) AS occupants
				FROM rooms
				LEFT JOIN fellows ON rooms.id = fellows.room_id
				WHERE rooms.type='L' GROUP BY rooms.id
				HAVING occupants < {0}""" .format(LivingRoom.room_capacity))
		elif room_type == "office":
			return self.db.select_all(
				"""SELECT rooms.id, rooms.name, rooms.type,
				COUNT(*) AS occupants
				FROM rooms
				LEFT JOIN staff ON rooms.id = staff.room_id
				WHERE rooms.type='O' GROUP BY rooms.id
				HAVING occupants < {0} """.format(OfficeRoom.room_capacity))

	def exists(self, room_type, room_id):
		"""
		Get the details of a living space

		Arguments:
				room_id The unique Id for the living space
		Returns:
			List    Record of a living space
		"""
		query = ''
		if isinstance(room_id, str):
			query += "SELECT * FROM rooms WHERE name = '%s' AND type='%s'" % (
				room_id, room_type)
		elif isinstance(room_id, int):
			query += "SELECT * FROM rooms where id = %d AND type='%s'" % (
				room_id, room_type)
		# import ipdb
		# ipdb.set_trace()
		room = self.db.select_one(query)

		if len(room)==0:
			return False
		return room


class OfficeRoom(Room):
	"""
	Specifies office space particulars

	"""
	room_capacity = 6

	def __init__(self):
		"""initialize the database"""
		super(self.__class__,self).__init__()
		# self.rooms = Room()
		# self.db = DbManager

class LivingRoom(Room):
	"""
	Specifies living space particulars

	"""
	room_capacity = 4

	def __init__(self):
		"""initialize the database"""
		super(self.__class__,self).__init__()
		# self.rooms = Room()
		# self.db = DbManager



