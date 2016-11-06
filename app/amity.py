import random
from app.rooms import OfficeSpace
from app.rooms import LivingSpace
from app.people import Staff
from app.people import Fellow
from termcolor import cprint, colored

class Amity(object):

    def __init__(self):
        self.all_people = []
        self.staff_list = []
        self.fellows_list = []
        self.allocated_people = []
        self.allocated_staff = []
        self.allocated_fellows = []
        self.unallocated_people = []
        self.all_rooms = []
        self.living_spaces = []
        self.office_spaces = []
        self.allocated_rooms = []
        self.db_people_list = []
        self.db_room_list = []

    def create_room(self, room):
        '''
        Confirm that the room name does not exist and create room.

        '''
        for rooms in self.all_rooms:
            if room["room_name"] == rooms.room_name:
                cprint (("\n"+rooms.room_name+" already exists. "), 'green')
                return
        if room["room_type"] == "office":
            new_room = OfficeSpace(room["room_name"])
            self.all_rooms.append(new_room)
            self.office_spaces.append(new_room)
            text = ("\n You have added "+new_room.room_name+" to Amity offices")
        else:
            new_room = LivingSpace(room["room_name"])
            self.all_rooms.append(new_room)
            self.living_spaces.append(new_room)
            text = ("\n You have added "+new_room.room_name+" to Living Spaces in Amity ")
        cprint ((text), 'green')

    def create_person(self, person):
        '''
        Once a person is created they are called by the assign person function
        to assign them an office room. 
        If the person is a fellow and wants accomodation, the assign fellow to living space function
        is also called. This is to automate room allocations.
        '''  
        for people in self.all_people:
            if person["person_name"] == people.person:
                cprint (("\n"+people.person+" a person with that name already exists."), 'green')
                return
        if person["role"] == "staff":
            new_person = Staff(person["person_name"]) 
            self.staff_list.append(new_person)
            cprint (("\n You have added "+new_person.person+" as a staff member in Amity."), 'green')
        else:
            new_person = Fellow(person["person_name"])
            new_person.accomodation = person["wants_accomodation"]
            self.fellows_list.append(new_person)
            cprint (("\n You have added "+new_person.person+" as a Fellow in Amity."), 'green')
            if new_person.accomodation in ["yes", "Y"]:
                self.assign_fellow_to_living_space(new_person)
            else: self.unallocated_people.append(new_person)
        self.all_people.append(new_person)
        self.assign_person_to_office_space(new_person)
        
    def assign_person_to_office_space(self, new_person):
        '''
        The functions first checks if an office is full before assigning a person
        to the room.
        '''
        if len(self.office_spaces) > 0:
            random_room = self.get_random_room("office")
            if self.is_room_available(random_room) == True:
                if type(new_person) == Staff:
                    self.allocated_staff.append(new_person)
                elif type(new_person) == Fellow:
                    if new_person not in self.allocated_fellows: self.allocated_fellows.append(new_person)                              
                random_room.occupants.append(new_person)
                new_person.assigned_office = random_room.room_name
                self.allocated_people.append(new_person)
                if random_room not in self.allocated_rooms: self.allocated_rooms.append(random_room)
                text = ("\n"+new_person.person+" has been assigned to "+random_room.room_name)
            else:
                text = ("\n"+random_room.room_name+" is full. "+new_person.person+" cannot be assigend here.")
                if new_person not in self.unallocated_people: self.unallocated_people.append(new_person)
        else:
            text = ("\n There are no office rooms in Amity. Create a room before adding people.")
            if new_person not in self.unallocated_people: self.unallocated_people.append(new_person)
        cprint ((text), 'green')
            
    def assign_fellow_to_living_space(self, new_person):
        if len(self.living_spaces) > 0:
            random_room = self.get_random_room("living")
            if self.is_room_available(random_room) == True:
                random_room.occupants.append(new_person)
                new_person.assigned_living = random_room.room_name
                if new_person not in self.allocated_fellows: self.allocated_fellows.append(new_person)
                if random_room not in self.allocated_rooms: self.allocated_rooms.append(random_room)
                text = ("\n"+new_person.person+" has been assigned to "+random_room.room_name)
            else:
                text = ("\n"+random_room.room_name+" is full. "+new_person.person+" create rooms before adding people.")
                if new_person not in self.unallocated_people: self.unallocated_people.append(new_person)
        else:
            text = ("\n There are no living rooms in Amity. Create rooms before adding people.")
            if new_person not in self.unallocated_people: self.unallocated_people.append(new_person)
        cprint ((text), 'green')

    def get_random_room(self, room_type):
        '''
        To pick a random room before assigning someone.

        '''
        if room_type == "office":
            random_room = self.office_spaces[random.randint(0, (len(self.office_spaces) -1))]
        else:
            random_room = self.living_spaces[random.randint(0, (len(self.living_spaces) -1))]
        return random_room

    def is_room_available(self, random_room):
        '''
        To ensure the room is not full.

        '''
        if random_room.room_type == "OfficeSpace":
            return len(random_room.occupants) < 6
        elif random_room.room_type == "LivingSpace":
            return len(random_room.occupants) < 4

    def reallocate_person(self, person, room_name):
        '''
        Checks if the room name provided quaifies to accomodate a person.

        '''
        rooms_list = [room.room_name for room in self.all_rooms]
        if room_name not in rooms_list:
            cprint (("\n"+room_name+" does not exist. \n"), 'green')
        elif room_name in [person.assigned_living, person.assigned_office]:
            cprint (("\n"+person.person+" is already assigned to "+room_name), 'green')
        else:
            room = [room for room in self.all_rooms if room.room_name == room_name][0]
            if type(person) == Staff and type(room) == LivingSpace:
                cprint(("\n Staff cannot be assigned to living spaces."), 'green')
            elif self.is_room_available(room):
                if type(room) == OfficeSpace:
                    self.clean_up_office_reallocations(person)
                    person.assigned_office = room.room_name
                    if person in self.unallocated_people:
                        if type(person) == Fellow: pass
                        else: self.unallocated_people.remove(person)
                elif type(room) == LivingSpace:
                    self.clean_up_living_reallocations(person)
                    person.assigned_living = room.room_name
                    if person in self.unallocated_people: self.unallocated_people.remove(person)
                room.occupants.append(person)
                if person not in self.allocated_people: self.allocated_people.append(person)
                if room not in self.allocated_rooms: self.allocated_rooms.append(room)
                cprint (("\n You have reallocated "+person.person+" to "+room.room_name+"."), 'green')
            else:
                cprint (("\n The " + room.room_name +" is full try another room."), 'green')                   
                        
    def clean_up_office_reallocations(self, person):
        '''
        Remove a person from their old office 
        '''
        old_office = person.assigned_office
        if old_office == "": pass
        else: 
            room = [room for room in self.all_rooms if room.room_name == old_office][0]
            room.occupants.remove(person)
            return room.occupants

    def clean_up_living_reallocations(self, person):
        '''
        Remove person from their old living space.

        '''
        old_living = person.assigned_living
        if old_living == "": pass
        else:
            room = [room for room in self.all_rooms if room.room_name == old_living][0]
            room.occupants.remove(person)
            return room.occupants

    def load_people_from_file(self, filename):
        '''To load people from a file'''
        with open("./app/"+filename, mode="r") as text:
            people_list = text.readlines()
            for people in people_list:
                person = people.split()
                person_name = person[0].lower()+" "+person[1].lower()
                role = person[2]
                if role == "STAFF":
                    person_dict = {"person_name":person_name, "role":"staff"}
                    self.create_person(person_dict)
                if role == "FELLOW":
                    accomodation = person[3]
                    person_dict = {"person_name":person_name, "role":"fellow", 
                    "wants_accomodation":accomodation}
                    self.create_person(person_dict)

    def write_allocated_to_terminal(self):
        '''Print allocated fellows to terminal'''
        if len(self.all_rooms) > 0:
            cprint (("\n Showing allocated people..."), 'green')
            for room in self.all_rooms:
                text = "\n"+room.room_name
                text = text + ("="*40 + "\n")           
                if len(room.occupants) > 0:
                    text = text + (", ".join([occupant.person for occupant in room.occupants])+"\n")
                else:
                    text = text + ("\n This room is empty")
                cprint ((text), 'green')
        else:
            cprint (("\n All rooms are empty. \n"), 'green')

    def write_allocated_to_file(self, filename):
        '''print allocated people to a file'''
        cprint (("\n Check allocations in: "+filename), 'red')
        with open(filename, mode="w", encoding='utf-8') as text:
            for room in self.all_rooms:
                text.write("\n"+room.room_name+"\n")
                text.write("-"*40 +"\n")            
                if len(room.occupants) > 0:
                    text.write(", ".join([occupant.person for occupant in room.occupants])+"\n")    
                else:
                    text.write("Room is empty! \n")
            
    def write_unallocated_to_terminal(self):
        '''Print a list of unallocated people on the terminal'''
        if len(self.unallocated_people) > 0:
            text = ("\n loading...\n")
            text = "\n Unallocated people:"+"\n"
            text = text + ("*"*40 + "\n")
            text = text + (", ".join([person.person for person in self.unallocated_people])+"\n")
        else: 
            text = ("\n Unallocated people do not exist.")
        cprint ((text), 'green')
            
    def write_unallocated_to_file(self, filename):
        '''print unallocated to a file'''
        cprint (("\n Check unallocated at: "+filename), 'green')
        with open(filename, mode="w", encoding='utf-8') as text:
            if len(self.unallocated_people) > 0:
                text.write("Unallocated people:"+"\n")
                text.write("="*40 +"\n")
                text.write(", ".join([person.person for person in self.unallocated_people]))
            else:
                text.write("There are no unallocated people at the moment.")

    def print_room(self, room_name):
        if len(self.all_rooms) > 0:
            for room in self.all_rooms:
                if room.room_name == room_name:
                    if len(room.occupants) > 0:
                        text = ("\n"+room.room_name)
                        text = text + ("*"*50 +"\n")
                        text = text + (", ".join([occupant.person for occupant in room.occupants])+"\n")
                    else:
                        text = ("\n This room is empty.")
        else:
            text = ("\n There are no that room yet.")    
        cprint ((text), 'green')

    def load_rooms_from_db(self, room):
        '''load rooms from db '''
        if room["room_type"] == "OfficeSpace":
            new_room = OfficeSpace(room["room_name"])
            self.office_spaces.append(new_room)
        else:
            new_room = LivingSpace(room["room_name"])
            self.living_spaces.append(new_room)
        self.db_room_list.append(new_room)
        self.all_rooms.append(new_room)

    def load_people_from_db(self, person, assigned_office, assigned_living):
        '''load people from db'''
        if person["role"] == "Staff":
            new_person = Staff(person["person_name"])
            new_person.assigned_office = assigned_office
            new_person.assigned_living = assigned_living
            self.staff_list.append(new_person)
            self.allocated_staff.append(new_person)
        else:
            new_person = Fellow(person["person_name"])
            new_person.assigned_office = assigned_office
            new_person.assigned_living = assigned_living
            self.fellows_list.append(new_person)
            self.allocated_fellows.append(new_person)
        self.db_people_list.append(new_person)
        self.all_people.append(new_person)
        self.allocated_people.append(new_person)

    def populate_room_occupants_from_db_load(self):
        '''
        Getting all the rooms and their occupants.
        '''
        for room in self.db_room_list:
            for person in self.db_people_list:
                if person.assigned_office == room.room_name:
                    room.occupants.append(person)
                elif person.assigned_living == room.room_name:
                    room.occupants.append(person)
                else:
                    if "" in [person.assigned_office, person.assigned_living]:
                        if person not in self.unallocated_people: self.unallocated_people.append(person)

            
    def get_list_of_rooms(self):
        return self.all_rooms   

    def get_list_of_living_spaces(self):
        return self.living_spaces

    def get_list_of_office_spaces(self):
        return self.office_spaces

    def get_list_of_allocated_rooms(self):
        return self.allocated_rooms

    def get_list_of_people(self):
        return self.all_people

    def get_list_of_staff(self):
        return self.staff_list

    def get_list_of_fellows(self):
        return self.fellows_list

    def get_list_of_allocated_people(self):
        return self.allocated_people

    def get_list_of_allocated_staff(self):
        return self.allocated_staff

    def get_list_of_allocated_fellows(self):
        return self.allocated_fellows
    
    def get_list_of_unallocated_people(self):
        return self.unallocated_people
    
    def get_list_of_db_rooms(self):
        return self.db_room_list

    def get_list_of_db_people(self):
        return self.db_people_list
