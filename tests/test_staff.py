import unittest
from app.people import Staff
from .mock_data import MockData

class PeopleTest(unittest.TestCase):
	"""Tests for Staff Class"""
	def setUp(self):
		self.data = MockData()

	def test_staff_table_exists(self):
		staff = self.data.fetch_data("staff", False)
		self.assertEqual(staff, [])


