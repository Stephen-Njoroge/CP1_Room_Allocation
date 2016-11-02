import unittest
from app.people import Staff
from .mock_data import MockData

class PeopleTest(unittest.TestCase):
	"""Tests for Staff Class"""
	def setUp(self):
		self.data = MockData()

	def test_staff_table_exists(self):
		staff = self.data.fetch_data("staff", False)
		self.assertTrue(staff)

	def test_a_user_can_add_staff(self):
		'''To test whether the system alerts a user if they add a staff member when there is no vacant space.''' 
		with self.assertRaises(ValueError) as e:
			staff_member = self.data.create_staff("Daniel", "Bower")
			self.assertEqual(
				'All rooms are full! Sorry Daniel Bower',
				e)
	def test_the_staff_member_added(self):
		'''Testing whether the member of staff has been created'''
		staff = self.data.fetch_data("staff", False)
		self.assertEqual(2, len(staff))
		self.assertEqual(staff[0][-1], None)

	def test_staff_member_allocated_room(self):
		'''Testing whether the system alloctes a room to a member of staff'''
		self.data.create_office_spaces(['Camelot'])
		self.data.create_staff("JOHN", "Thuo")
		staff_members = self.data.fetch_data('staff', False)
		self.assertEqual(staff_members[1][-1], 3)

	def test_reallocate_staff(self):
		'''To check whether the system can relocate a member of staff to a non existent room'''
		staff = Staff()
		with self.assertRaises(ValueError) as e:
			staff.relocate(
				{'fellow': False, 'staff': True, '<person_identifier>': 2,
				 '<new_room_name>': 'graber'})
			self.assertEqual("A room with that name does not exist.", e)

	def test_reallocate_non_existent_staff(self):
		'''relocating a non existent staff.'''
		staff = Staff()
		with self.assertRaises(ValueError) as e:
			staff.relocate(
				{'fellow': False, 'staff': True, '<person_identifier>': 10,
				 '<new_room_name>': 'graber'})
			self.assertEqual("Staff member with that name does not exist.", e)

	def test_succesfully_reallocate_staff(self):
		'''To see if the system can relocate a staff member given the right params.'''
		self.data.create_office_spaces(['midgar'])
		staff = Staff()
		staff.relocate(
			{'fellow': False, 'staff': True, '<person_identifier>': 2,
			'<new_room_name>': 'midgar'})
		staff_members = self.data.fetch_data('staff', False)
		self.assertEqual(staff_members[1][-1], 4)

	

	def tearDown(self):
		"""Delete the test database"""
		self.data.clear_test_db()

if __name__ == '__main__':
	unittest.main()




