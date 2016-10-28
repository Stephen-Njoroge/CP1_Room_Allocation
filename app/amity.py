"""
RoomAllocator

Room allocation useful commands

Usage:
	amity create_rooms (living|office) <room_name>...
	amity add_person <first_name> <last_name> (fellow|staff) [--a=n]
	amity reallocate_person (fellow|staff) <person_identifier> <new_room_name>
	amity print_allocations [--o=allocations.txt]
	amity print_room <room_name> [--o=y]
	amity load_people
	amity (-i | --interactive)
	amity (-h | --help | --version)
Options:
	-i, --interactive  Interactive Mode
	-h, --help  Show this screen and exit.
"""
import cmd
import sys
from docopt import docopt, DocoptExit
from rooms import Room
from people import Person, Staff, Fellow

class DocoptLanguageError(Exception):

    """Error in construction of usage-message by developer."""


def pass_opt(func):
	"""
	Used to avoid repeating try and except on every docopt option.
	"""
	def fn(self, arg):
		try:
			opt = docopt(fn.__doc__, arg)

		except DocoptExit as e:
			# When a user inputs an invalid command
			# Prints the command doesn't exist

			print('Invalid Command!')
			print(e)
			return

		except SystemExit:
			# automatically prints --h for help

			return

		return func(self, opt)

	fn.__name__ = func.__name__
	fn.__doc__ = func.__doc__
	fn.__dict__.update(func.__dict__)
	return fn

class Amity(cmd.Cmd):
	"""The program's functionalities come here in the end"""
	intro = """Welcome! This is Amity room allocation (type help for a list of commands.)"""

	prompt = '(amity) '
	file = None

	@pass_opt
	def do_create_rooms(self, args):
		"""Usage: create_rooms (living|office) <room_name>..."""
		try:
			print(Room().create_room(args))
		except ValueError as e:
			print(e)

	@pass_opt
	def do_add_person(self, args):
		"""Usage: add_person <first_name> <last_name> (fellow|staff) [--a=n]"""
		try:
			if args['fellow']:
				fellow = Fellow()
				print(fellow.add_fellow(args))
			else:
				staff = Staff()
				print(staff.add_staff(args))
		except ValueError as e:
			print(e)

	@pass_opt
	def do_reallocate_person(self, args):
		"""Usage: reallocate_person (fellow|staff) <person_identifier> <new_room_name>"""
		try:
			if args['fellow']:
				print(Fellow().relocate(args))
			else:
				print(Staff().relocate(args))
		except ValueError as e:
			print(e)

	@pass_opt
	def do_print_allocations(self, args):
		"""Usage: print_allocations [--o=y]"""
		rooms = Room()
		try:
			print(rooms.show_all_allocations(args))
		except ValueError as e:
			print('Error')

	@pass_opt
	def do_print_room(self, args):
		"""Usage: print_room <room_name> [--o=y]"""
		try:
			rooms = Room()
			print(rooms.show_particular_room_allocation(args))
		except ValueError as e:
			print(e)

	@pass_opt
	def do_print_unallocated(self, args):
		"""Usage: print_unallocated [--o=y]"""
		try:
			person = Person()
			person.all_unallocated(args)
		except ValueError as e:
			print(e)

	@pass_opt
	def do_load_people(self, args):
		"""Usage: load_people"""
		try:
			people = Person()
			people.allocations_from_file(args)
		except ValueError as e:
			print(e)

	def do_quit(self, arg):
		"""Quits out of Interactive Mode."""
		print('Thankyou!')
		exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
	Amity().cmdloop()

print(opt)

		