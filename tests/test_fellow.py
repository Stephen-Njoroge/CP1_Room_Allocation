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
        self.assertIn(('John'), fellows)
        
    def tearDown(self):
        """Delete the test database"""
        self.data.clear_test_db()

if __name__ == '__main__':
    unittest.main()
