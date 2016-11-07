[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9b150efb71394b1eaa974a2e60f1bf7c)](https://www.codacy.com/app/stephen-njoroge/CP1_Room_Allocation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Stephen-Njoroge/CP1_Room_Allocation&amp;utm_campaign=Badge_Grade)
# CP1_Room_Allocation


```
Amity is Room allocation system for Andela Accomodation and Offices facility.

```

Amity enables a user to manage the living and office spaces by allocating the fellows and staff members respectively.

Amity works under the following constraints

1. An office can occupy a maximum of 6 people.
2. A living space can inhabit a maximum of 4 people.
3. A person to be allocated could be a fellow or staff.
4. Staff cannot be allocated living spaces.
5. Fellows have a choice to choose a living space or not.

## Installation

To set up amity, make sure that you have python3 and pip3 installed on your system.

It is also appropriate to ensure you have a virtual environment so as to avoid installing unnecessary packages on your system.

Proceed to clone this repo into your projects folder

```bash
$ git clone https://github.com/Stephen-Njoroge/CP1_Room_Allocation.git

$ cd CP1_Room_Allocation
```

Create a virtual environment to work from using the `python3 -m venv my-venv` command

```bash
$ python3 -m venv my-venv
```

This will automagically activate the virtual env. You can now proceed to install all modules used from the `requirements.txt` file

```bash
 $ pip install -r requirements.txt
```

Confirm your installed packages
```bash
$ pip freeze
```

## Usage

To get the app running, run the entry script file with an `--i` or `--interactive` option

```bash
$ python app.py -i
```

or
```bash
$ python app.py --interactive
```

**1. Create Rooms**

To create a living or office space, follow the following docopt pattern
```bash
Usage: create_room <room_name>...
```

Creating rooms
```bash
create_room scala php go
```

**2. Add Person**

You can either add a staff member or a fellow with the `add_person` command.
A fellow can either opt in or out of the Amity accomodation plan.
The docopt patter is as follows
```bash
Usage: add_person <first_name> <last_name> [--accomodation=n]
```

Add a staff member
```bash
add_person Joshua Mwaniki 
```

Add a fellow that opts in to the andela accommodation
```bash
add_person Daniel Migwi fellow --accomodation=y
```

Add a fellow that opts out of the andela accommodation
```bash
add_person Rehema Wachira --accomodation=n
```

**3. Reallocate a person**

You can reallocate a person from one space (living or office) to another using the following pattern
```bash
reallocate_person <person_identifier>
```

Reallocate a fellow with id 1 from swift to scala

```bash
reallocate_person John Migwi
```

**4. Print out data**

The print methods allow you to print out room allocations for all rooms, one room or list of unallocated people.
You can also specify an optional `--o` parameter to write the data to a file.

**Print room allocations**

Print out a list of all room allocations at amity
```bash
print_allocations --o=file_name.txt
```
**Print unallocated**

Print out a list of all unallocated people (staff members and fellows)
```bash
print_unallocated --o=filename.txt
```

**Print out room details**

Print out a list of the allocations of a particular room at amity
```bash
print_room camelot --o=y
```

**Load all data that is in the database to the application**

loads all app data into the application
```bash
load_state
```

**5. Load people from file**

Adds people to rooms from a txt file
```bash
load_people
```
**6. Quit!**
To exit from the application, simply type `quit` on yout room-alloc app
```bash
quit
```

**7. Save data in the application to a new database**

saves app data to a specified database
```bash
save_state
```

You can get out of the Virtual environment by simply typing `deactivate` on your commandline

## Contributing

Contributions are **welcome** and will be fully **credited**.

We accept contributions via Pull Requests on [Github](https://github.com/Stephen-Njoroge/CP1_Room_Allocation.git).

## Donations

If you feel philanthropic, contact[ Stephen Njoroge](mailto:stephen.njoroge@andela.com) or create an issue.


## License

### The MIT License (MIT)

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.

