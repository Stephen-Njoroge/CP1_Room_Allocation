import unittest
from app import people
from mock_data import MockData

class PeopleTest(unittest.Testcase):
	"""
	Holds tests for the Fellow class

	"""

	def test_create_a_fellow(self):
		"""
		Checking whether a user can create a fellow
		"""
		fellow_instance = self.mock_data.create_fellow("Stephen", "Njoroge", "Y")
		self.assertTrue(fellow_instance)



if __name__ == '__main__':
    unittest.main()
