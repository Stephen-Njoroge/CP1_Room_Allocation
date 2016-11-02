import unittest
from app.people import Fellow
from .mock_data import MockData

class PeopleTest(unittest.TestCase):
	"""Tests for Fellow class"""

	def setUp(self):
		self.data = MockData()

	def test_fellows_table_exist(self):
		'''To test a the fellows table exist'''
		fellows = self.data.fetch_data('fellows', False)
		self.assertTrue(fellows)

	def test_a_user_can_add_fellow(self):
		'''To test whether a user can add a fellow''' 
		new_fellow = self.data.create_fellow("STEPHEN", "NJOROGE", "n")
		self.assertTrue(new_fellow)

	def test_fellow_exists_in_db(self):
		'''To see that the fellow is saved in the db'''
		fellows = self.data.fetch_data('fellows', False)
		self.assertIn('Stephen Njoroge', fellows[0])

	def test_accomodate_fellow(self):
		'''To check whether the system accomodates a fellow'''
		self.data.create_living_spaces(['swift'])
		self.data.create_fellow("JOHN", "MAINA", "y")
		fellows = self.data.fetch_data('fellows', False)
		self.assertFalse(fellows[0][-1], None)

	def test_reallocate_fellow(self):
		'''To check whether the system can relocate a fellow to a non existent room'''
		fellow = Fellow()
		with self.assertRaises(ValueError) as e:
			fellow.relocate(
				{'fellow': True, 'staff': False, '<person_identifier>': 2,
				 '<new_room_name>': 'camelot'})
			self.assertEqual("A room with that name does not exist.", e)

	def test_reallocate_non_existent_fellow(self):
		'''relocating a non existent fellow.'''
		fellow = Fellow()
		with self.assertRaises(ValueError) as e:
			fellow.relocate(
				{'fellow': True, 'staff': False, '<person_identifier>': 10,
				 '<new_room_name>': 'swift'})
			self.assertEqual("A fellow with that name does not exist.", e)
	def test_succesfully_reallocate_fellow(self):
		'''To see if the system can relocate a fellow given the right params.'''
		self.data.create_living_spaces(['heroku'])
		fellow = Fellow()
		fellow.relocate(
			{'fellow': True, 'staff': False, '<person_identifier>': 2,
			'<new_room_name>': 'heroku'})
		fellows = self.data.fetch_data('fellows', False)
		self.assertEqual(fellows[1][-1], 2)
	def test_unallocated_fellow(self):
		'''Checking whether the system can add a fellow with no accomodation'''
		self.data.create_fellow("Robert", "Kibui", "n")
		fellow = Fellow()
		unallocated_fellows = fellow.unallocated_employees("fellow")
		self.assertEqual(2, len(unallocated_fellows))

	def tearDown(self):
		"""Delete the test database"""
		self.data.clear_test_db()

if __name__ == '__main__':
	unittest.main()
