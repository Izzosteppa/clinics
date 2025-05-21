import unittest
from datetime import datetime
from unittest.mock import patch

from clinician_booker_options.clinician_options import (
    help_to_get_open_slots,
    user_date_class)

class TestYourFunctions(unittest.TestCase):

    def test_user_date_class(self):
        """Checks if the function returns the correct start date and start time."""

        with patch('logic_code.user_input.get_valid_date_input', return_value=("2024", "03", "01")), \
             patch('logic_code.user_input.valid_time_input', return_value=("10", "00")):
            start_date, start_time = user_date_class("2024-03-01", "10:00:00")
            self.assertEqual(start_date, datetime(2024, 3, 1, 0, 0, 0))
            self.assertEqual(start_time, datetime(2024, 3, 1, 10, 0, 0))


class TestHelpToGetOpenSlots(unittest.TestCase):
    def test_no_attendees(self):
        """Checks if the function returns True when there are no attendees."""
        
        event_data = {"Event Attendee": "No Attendees"}
        self.assertTrue(help_to_get_open_slots(event_data))

    def test_with_attendees(self):
        """Checks if the function returns False when there are attendees."""
        
        event_data = {"Event Attendee": "Alex Jay"}
        self.assertFalse(help_to_get_open_slots(event_data))

    def test_empty_data(self):
        """Checks if the function returns False when given empty data."""
        event_data = {}
        self.assertFalse(help_to_get_open_slots(event_data))

    def test_multiple_attendees(self):
        """ Checks if the function returns False when there are multiple attendees."""
        
        event_data = {"Event Attendee": "Alex Jay", "Event Location": "WTC_CPT"}
        self.assertFalse(help_to_get_open_slots(event_data))



if __name__ == '__main__':
    unittest.main()


