import unittest
from logic_code.user_input import get_valid_date_input, get_username, valid_time_input


class TestUserInputFunctions(unittest.TestCase):

    def test_get_valid_date_input_valid(self):
        """Test get valid date input function."""
        date_str = '2024-02-14'
        expected_output = ('2024', '2', '14')
        self.assertEqual(get_valid_date_input(date_str), expected_output)

    def test_get_valid_date_input_invalid_format(self):
        """Test date format validation."""
        date_str = '2024/02/14'
        with self.assertRaises(SystemExit):
            get_valid_date_input(date_str)

    def test_get_username_valid(self):
        """Test username validation."""
        username = 'jay023'
        expected_output = 'jay023@student.wethinkcode.co.za'
        self.assertEqual(get_username(username), expected_output)

    def test_get_username_invalid(self):
        """Test invalid username."""
        username = 'invalid'
        with self.assertRaises(SystemExit):
            get_username(username)

    def test_valid_time_input_valid(self):
        """Test valid time input."""
        time_input = '12:30'
        expected_output = ['12', '30']
        self.assertEqual(valid_time_input(time_input), expected_output)

    def test_valid_time_input_invalid_format(self):
        """Test invalid time format."""
        time_input = '1230'
        with self.assertRaises(SystemExit):
            valid_time_input(time_input)
