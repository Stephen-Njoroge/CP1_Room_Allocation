import unittest
from app.rooms import Room
from .mock_data import MockData

class PeopleTest(unittest.TestCase):
	"""Tests for Rooms class"""

	def setUp(self):
		self.data = MockData()

	def test_rooms_exist(self)