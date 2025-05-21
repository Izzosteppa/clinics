from googleapiclient.errors import HttpError
import logic_code.user_input as ui
from logic_code.user_input import get_custom_date_event_creation_1


def creation_of_event(service, cal_ID, start_of_other_events):
    """Creates an event and returns the event. Prevents double-booking."""
    starting_ending = get_custom_date_event_creation_1()
    if not start_of_other_events:
        return "\033[1;31;10mThis slot has been taken. Choose another time.\033[0m"
    event = {
        "summary": "Opened slot",
        "description": "Open slot",
        "location":ui.command_line()[5],
        "start": {
            "dateTime": starting_ending[0] + ":00",
            "timeZone": "Africa/Johannesburg",
        },
        "end": {
            "dateTime": starting_ending[1] + ":00",
            "timeZone": "Africa/Johannesburg",
        },
    }
    for i in (cal_ID, "primary"):
        service.events().insert(calendarId=i, body=event,sendUpdates="all").execute()
    return "\033[1;32;10mYou have successfully created a slot.\033[0m"


def delete_event(service, event_id, cal_ID, list_p_cc):
    """Deletes an event in code clinics calendar as well as the primary."""
    new_ls_ids = list_p_cc
    for i in new_ls_ids:
        if event_id in i:
            try:
                service.events().delete(calendarId=i[2], eventId=i[1],sendUpdates="all").execute()
                service.events().delete(calendarId=cal_ID, eventId=i[0],sendUpdates="all").execute()
                return
            except HttpError as err:
                pass
    print("\033[1;34;10mPlease ask your teammates to to give you all rights to their primary calendar\033[0m")
    print("\033[1;34;10mThis event will only be deleted in your code_clinics calendar\033[0m")
    service.events().delete(calendarId=cal_ID, eventId=event_id,sendUpdates="all").execute()


def update_event(service, event_id, cal_ID, event_descri, booker_email, primary_cal_info):
    """Updates an empty event into a booked slot."""

    event_1 = {
        "summary": "Slot booked",
        "description": event_descri,
        "attendees": [{"email": booker_email}],
    }
    new_ls_ids=primary_cal_info
    for i in new_ls_ids:
        if event_id in i:
            try:
                service.events().patch(calendarId=i[2], eventId=i[1], body=event_1, sendUpdates="all").execute()
                service.events().patch(calendarId=cal_ID, eventId=i[0], body=event_1, sendUpdates="all").execute()
                return
            except HttpError as err:
                pass
    print("\033[1;34;10mPlease ask your teammates to to give you all rights to their primary calendars\033[0m")
    print("\033[1;34;10mThis event will only be deleted in your code_clinics calendar\033[0m")
    service.events().patch(calendarId=cal_ID, eventId=event_id, body=event_1, sendUpdates="all").execute()


def cancel_booked_slot(service, event_id, cal_ID, primary_cal_info):
    """Modifies the booked slot and returns the event with only the volunteer's email."""

    event_1 = {"summary": "Opened slot", "description": "Open slot", "attendees": ""}
    new_ls_ids = primary_cal_info
    for i in new_ls_ids:
        if event_id in i:
            try:
                service.events().patch(
                    calendarId=i[2], eventId=i[1], body=event_1, sendUpdates="all"
                ).execute()
                service.events().patch(
                    calendarId=cal_ID, eventId=i[0], body=event_1, sendUpdates="all"
                ).execute()
                return
            except HttpError as err:
                pass
    print("\033[1;34;10mPlease ask your teammates to to give you all rights to their primary calendars.\033[0m")
    print("\033[1;34;10mThis event will only be deleted in your code_clinics calendar.\033[0m")
    service.events().patch(calendarId=cal_ID, eventId=event_id, body=event_1, sendUpdates="all").execute()
