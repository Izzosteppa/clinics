from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta

import logic_code.user_input as ui
from data_handling.data_visualizer import displaydata


def view_your_schedule_open(result, email):
    """Views the volunteer's open slot schedule."""
    count = 0
    for event_data in result:
        if help_to_get_open_slots(event_data) and get_doctors_email(event_data, email):
            count += 1
            table = Table()
            for key, value in event_data.items():
                if key != "Event Description":
                    if key != "Event ID":
                        displaydata(key, value, table, count)
            console = Console()
            console.print(table)
    if count == 0:
        print(f"\033[1;31;10mNo open slots for {email} try, '-a AddSlot'.\033[0m")
    else:
        print(f"\033[1;36;10mYou can cancel your empty slots with '-a CancelEmptySlot'.\033[0m")


def help_to_get_open_slots(event_data):
    """Checks if there are any attendees."""
    for key, value in event_data.items():
        if key == "Event Attendee":
            if value == "No Attendees":
                return True
    return False


def user_date_class(user_date,user_time):
    """Gets the start date and start time of the event."""
    year, month, day = ui.get_valid_date_input(user_date)
    hour, minute = ui.valid_time_input(user_time)
    start_date = datetime(int(year), int(month), int(day), 0, 0, 00)
    start_time = datetime(int(year), int(month), int(day), int(hour), int(minute), 00)
    return start_date,start_time


def adding_slot_validator(result):
    """Validates the slot added and prevents double-booking."""
    time_list = []

    for event_data in result:
        for key, value in event_data.items():
            if key == "Event Start Time":
                time_list.append(value)

    for i in time_list:
        year, month, day = ui.get_valid_date_input(i.split('T')[0])
        hour, minute = ui.valid_time_input(i.split('T')[1])
        start_time_event = datetime(int(year), int(month), int(day), int(hour), int(minute), 00)
        start_date_event = datetime(int(year), int(month), int(day), 0, 0, 00)
        user_dt,user_time = user_date_class(ui.get_custom_date_event_creation_1()[0].split("T")[0],ui.get_custom_date_event_creation_1()[0].split("T")[1])
        
        if user_dt == start_date_event:
            if user_time >= (start_time_event) and user_time <= (start_time_event + timedelta(minutes = 34)):
                return False

            if user_time <= (start_time_event) and (user_time) >= (start_time_event - timedelta(minutes = 30)):
                return False
    return True

def get_doctors_email(event_data, email):
    """Getting the volunteer's email."""
    for key, value in event_data.items():
        if key == "Event Creator Email":
            if value == email:
                return True
    return False

def valid_appointments(result, email):
    """Checks the volunteer's email and checks if there is a booker in the event."""
    count = 0
    for event_data in result:
        if help_to_get_open_slots(event_data) == False and get_doctors_email(
            event_data, email
        ):
            count += 1
            table = Table()
            for key, value in event_data.items():
                if key != "Event ID":
                    displaydata(key, value, table, count)
            console = Console()
            console.print(table)
    if count == 0:
        print(f"\033[1;31;10mYou have no booked slots available within {ui.command_line()[4]} days.\033[0m")
    else:
        print("\033[1;36;10mYou can add slots with '-a AddSlot'\033[0m")


def cancel_slot(result, email):
    """Cancels a volunteer's empty slot by deleting the event."""
    event_ls1 = [""]
    count = 0
    for event_data in result:
        if help_to_get_open_slots(event_data) and get_doctors_email(event_data, email):
            count += 1
            table = Table()
            for key, value in event_data.items():
                if key == "Event ID":
                    event_ls1.append(value)
                elif key != "Event Description":
                    displaydata(key, value, table, count)
            console = Console()
            console.print(table)
    if count >= 1:
        event_id_col = ui.menu_select(event_ls1[1:])
        return event_id_col
    if count == 0:
        print(f"\033[1;31;10mNo events to cancel within {ui.command_line()[4]} days.\033[0m")
    else:
        print("\033[1;36;10mYou can add slots with '-a AddSlot'.\033[0m")
        return 
