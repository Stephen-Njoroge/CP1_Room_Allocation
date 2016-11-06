
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
    amity save_state [--db=sqalchemy_database]
    amity load_state <sqalchemy_database>
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import cmd
import sys
import os
from docopt import docopt, DocoptExit
from app.db_commands import Database, amity
from termcolor import cprint, colored
from pyfiglet import figlet_format

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
            # Also gives a proper command.

            cprint(('\nInvalid Command!'), 'magenta')
            cprint(e, 'magenta')
            print('\n')
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
    intro= os.system("clear")
    cprint(figlet_format('WELCOME TO AMITY  R.A', font='slant', justify = 'centre'),
        'red', attrs=['bold', 'blink'])
    colored(__doc__)
    cprint("Type help for a list of commands. \n", 'green' )

    prompt = ''
    file = None

    @pass_opt
    def do_create_room(self, arg):
        """
        Creates a room in Amity. A room can either be an office or living space.
        Create as many rooms as possible by specifying multiple room names
        after the create_room command.
        
        Usage:
            create_room <room_name>...
        """
        try:
            for room in arg["<room_name>"]:
                print ("Room Name: "+room)
                room_type = input("Enter a room type, either 'office' or 'living': ")
                if room_type in ["office", "living"]:
                    amity.create_room({"room_name": room, "room_type": room_type})

        except ValueError as e:
            cprint(e, 'red')

    @pass_opt
    def do_add_person(self, arg):
        """
        Creates a person and assign them to a room in Amity. 

        Usage:
            add_person <first_name> <last_name> [--accomodation=n]
        """
        try:
            person = arg["<first_name>"] + " " + arg["<last_name>"]
            wants_accomodation = arg["--accomodation"]
            print ("Name: "+person)
            person_type = input("Enter a role, either 'staff' or 'fellow': ")
            if wants_accomodation in ["yes", "Y", "no", 'n', 'N']: print ("Wants Accomodation: "+wants_accomodation)
            if person_type in ["staff", "fellow"]: amity.create_person(
                {"person_name": person, "role": person_type, "wants_accomodation": wants_accomodation})
        except ValueError as e:
            cprint((e), 'red')

    @pass_opt
    def do_reallocate_person(self, arg):
        """
        Reallocates a person from their current room to another room.

        Usage:
            reallocate_person <first_name> <last_name> 
        """
        try:
            person_name = arg["<first_name>"] + " " + arg["<last_name>"]
            person = self.get_person(person_name)
            if person:
                print("Name: "+person.person)
                new_room = input("Enter the name of the new room: ")
                amity.reallocate_person(person, new_room) 
        except ValueError as e:
            cprint(e, 'red')

  
    def get_person(self, person_name):
        '''
        This is a helper function that verifies the person entered 
        exists in the list of all people. 
        '''
        try:
            names = [person.person for person in amity.all_people]
            if person_name not in names: return False
            else: 
                person = [person for person in amity.all_people if person.person == person_name][0]
                return person
        except ValueError as e:
            cprint('Error', 'red')

    @pass_opt
    def do_load_people(self, arg):
        '''
        Add people to rooms from a txt file.

        Usage:
            load_people <filename>
        '''
        try:
            amity.load_people_from_file(arg["<filename>"])
        except ValueError as e:
            cprint(e, 'red')

    @pass_opt
    def do_print_allocations(self, arg):
        '''
        Print the room and people allocations.

        Usage: 
            print_allocations [--o=filename]
        '''
        try:
            if arg["--o"]: amity.write_allocated_to_file(arg["--o"])
            else: amity.write_allocated_to_terminal()
        except ValueError as e:
            cprint(e, 'red')

    @pass_opt
    def do_print_unallocated(self, arg):
        '''
        Print the people who have not been allocated a room.

        Usage: 
            print_unallocated [--o=filename]
        '''
        try:
            if arg["--o"]: amity.write_unallocated_to_file(arg["--o"])
            else: amity.write_unallocated_to_terminal()
        except ValueError as e:
            cprint(e, 'red')

    @pass_opt
    def do_print_room(self, arg):
        '''
        Print the people allocated to a specified room.

        Usage:
            print_room <room_name>
        '''
        try:
            amity.print_room(arg["<room_name>"])
        except ValueError as e:
            cprint(e, 'red')

    @pass_opt
    def do_save_state(self, arg):
        '''
        Save all the data in the app to a SQAlchemy database. 
        Specifying the --db parameter explicitly stores the data
        in the database specified.

        Usage:
            save_state [--db=sqalchemy_database]
        '''
        try:
            db_name = arg['--db'] or 'amity.db'
            database.save_state(db_name)
            print ("The application data has been saved to "+db_name+"\n")
        except ValueError as e:
            cprint(e, 'red')
    @pass_opt
    def do_load_state(self, arg):
        '''
        Loads data from a specified database into the application.

        Usage:
            load_state <sqalchemy_database>
        '''
        try:
            database.load_state(arg["<sqalchemy_database>"])
            print ("\n The application data has been loaded from "+arg["<sqalchemy_database>"]+"\n")
        except ValueError as e:
            cprint(e, 'red')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        cprint(('Thankyou for Using Amity R.A Sytem!'), 'yellow')
        print u"\U0001F602" u" \U0001F602" u" \U0001F602"
        cprint (('#TIA'), 'blue')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amity().cmdloop()

print(opt)

        