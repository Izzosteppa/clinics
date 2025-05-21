
import unittest
from datetime import datetime, timedelta
from data_handling.data_modifier import extract_event_data, extract_calendar_data_for_cal_ID


class TestExtractEventData(unittest.TestCase):
    def test_valid_event_data(self):
        '''
        This test case verifies that the 'extract_event_data' method correctly extracts and refines event data from the data list. 
        It checks if the extracted data matches the expected data.
        '''
        data_list = [
            {
                "id": "1",
                "summary": "Event 1",
                "description": "Description 1",
                "location": "Room 101",
                "start": {"dateTime": "2023-04-01T09:00:00+02:00"},
                "end": {"dateTime": "2023-04-01T10:00:00+02:00"},
                "creator": {"email": "creator1@example.com"},
                "attendees": [{"email": "attendee1@example.com"}, {"email": "creator1@example.com"}]
            }
        ]
        campus = 'Main Campus'
        expected = [
            {
                "Event ID": "1",
                "Event Summary": "Event 1",
                "Event Description": "Description 1",
                "Event Location": "Room 101",
                "Event Start Time": "2023-04-01T09:00",
                "Event End Time": "2023-04-01T10:00",
                "Event Creator Email": "creator1@example.com",
                "Event Attendee": "attendee1@example.com",
            }
        ]
        result = extract_event_data(data_list, campus)
        self.assertEqual(result, expected)

    def test_missing_summary_description_location(self):
        '''Test for the scenario where the summary, description, and location are missing from the event data.'''
        data_list = [
            {
                "id": "2",
                "start": {"dateTime": "2023-04-02T09:00:00+02:00"},
                "end": {"dateTime": "2023-04-02T10:00:00+02:00"},
                "creator": {"email": "creator2@example.com"},
                "attendees": []
            }
        ]
        campus = 'Main Campus'
        expected = [
            {
                "Event ID": "2",
                "Event Summary": "No Title",
                "Event Description": "No Description",
                "Event Location": "Main Campus",
                "Event Start Time": "2023-04-02T09:00",
                "Event End Time": "2023-04-02T10:00",
                "Event Creator Email": "creator2@example.com",
                "Event Attendee": "No Attendees",
            }
        ]
        result = extract_event_data(data_list, campus)
        self.assertEqual(result, expected)

    def test_only_dates_provided(self):
        '''Test for the dates provided'''
        data_list = [
            {
                "id": "3",
                "start": {"date": "2023-04-03"},
                "end": {"date": "2023-04-03"},
                "creator": {"email": "creator3@example.com"},
                "attendees": []
            }
        ]
        campus = 'Main Campus'
        expected = [
            {
                "Event ID": "3",
                "Event Summary": "No Title",
                "Event Description": "No Description",
                "Event Location": "Main Campus",
                "Event Start Time": "2023-04-03T00:00",
                "Event End Time": "2023-04-03T23:59",
                "Event Creator Email": "creator3@example.com",
                "Event Attendee": "No Attendees",
            }
        ]
        result = extract_event_data(data_list, campus)
        self.assertEqual(result, expected)


    def test_no_attendees_creator_email(self):
        '''Test for the scenario where there are no attendees other than the creator of the event.'''

        data_list = [
            {
                "id": "4",
                "summary": "Event 4",
                "description": "Description 4",
                "location": "Room 404",
                "start": {"date": "2023-04-04"},
                "end": {"date": "2023-04-04"},
                "creator": {"email": "creator4@example.com"},
                "attendees": [{"email": "creator4@example.com"}]
            }
        ]
        campus = 'Main Campus'
        expected = [
            {
                "Event ID": "4",
                "Event Summary": "Event 4",
                "Event Description": "Description 4",
                "Event Location": "Room 404",
                "Event Start Time": "2023-04-04T00:00",
                "Event End Time": "2023-04-04T23:59",
                "Event Creator Email": "creator4@example.com",
                "Event Attendee": "No Attendees",
            }
        ]
        result = extract_event_data(data_list, campus)
        self.assertEqual(result, expected)



class TestExtractCalendarDataForCalID(unittest.TestCase):
    def test_valid_calendar_data(self):
        '''Test case for the 'extract_calendar_data_for_cal_ID' method.
        This test case verifies the correctness of the 'extract_calendar_data_for_cal_ID' method by testing it with valid calendar data. 
        It checks if the method correctly extracts the calendar data and the real user email.
        '''
        calendar_data = {
            "items": [
                {"id": "cal_1", "summary": "Calendar 1"},
                {"id": "cal_2", "summary": "Calendar 2", "primary": True}
            ]
        }
        expected_data = [
            {"calendar 1": "cal_1"},
            {"calendar 2": "cal_2"}
        ]
        expected_email = "cal_2"
        extracted_data, real_user_email = extract_calendar_data_for_cal_ID(calendar_data)

        self.assertEqual(extracted_data, expected_data)
        self.assertEqual(real_user_email, expected_email)

    def test_missing_summary_primary(self):
        '''
        This test case verifies the correctness of the 'test_missing_summary_primary' method by testing it
        with calendar data that has a missing 'summary' field for one of the calendar items. 
        It checks if the method correctly handles the missing 'summary' field and extracts
        the calendar data and the real user email.
    '''
        calendar_data = {
            "items": [
                {"id": "cal_3"},
                {"id": "cal_4", "summary": "Primary Calendar", "primary": True}
            ]
        }
        expected_data = extract_event_data, extract_calendar_data_for_cal_ID


    


if __name__ == '__main__':
    unittest.main()
from data_handling.data_modifier import extract_event_data, extract_calendar_data_for_cal_ID
