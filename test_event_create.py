import unittest
from unittest.mock import MagicMock
from datetime import datetime
from googleapiclient.errors import HttpError
from logic_code.event_creatie_update_del import *

class TestGoogleCalendarFunctions(unittest.TestCase):
    def setUp(self):
        """Setup for the programs."""
        self.service = MagicMock()
        self.cal_ID = "primary"
        self.start_of_other_events = ["2024-02-20T10:00:00", "2024-02-20T11:00:00"]
        self.event_id = "123456789"
        self.list_p_cc = [["1234567890", "0987654321", "secondary"], ["0987654321", "1234567890", "primary"]]
        self.booker_email = "user@example.com"
        self.primary_cal_info = [["111222333", "444555666", "secondary"], ["444555666", "111222333", "primary"]]


    def test_delete_event(self):
        """A test to check if the program is able to delete an event."""
        self.service.events().delete().execute.return_value = {}
        delete_event(self.service, self.event_id, self.cal_ID, self.list_p_cc)
        self.assertTrue(self.service.events().delete.called)


    def test_update_event(self):
        """Tests if the program updates events."""
        self.service.events().patch().execute.return_value = {}
        update_event(self.service, self.event_id, self.cal_ID, "Test Description", self.booker_email, self.primary_cal_info)
        self.assertTrue(self.service.events().patch.called)


    def test_cancel_booked_slot(self):
        """Testing if the booker can successfully cancel the slot."""
        self.service.events().patch().execute.return_value = {}
        cancel_booked_slot(self.service, self.event_id, self.cal_ID, self.primary_cal_info)
        self.assertTrue(self.service.events().patch.called)


if __name__ == "__main__":
    unittest.main()
