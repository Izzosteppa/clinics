from rich.console import Console
from rich.table import Table
from clinician_booker_options.clinician_options import help_to_get_open_slots, get_doctors_email

import logic_code.user_input as ui
from data_handling.data_visualizer import displaydata


def getting_a_slot(result, email):
    """ Shows the table and allows the user to get an open slot."""

    event_ls1 = [""]
    count = 0
    for event_data in result:
        if get_doctors_email(event_data, email) == False:
            if help_to_get_open_slots(event_data
            ) and not func_helper_to_get_attendees_email(event_data, email):
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
        print(f"\033[1;31;10mNo slots available for {ui.command_line()[4]} days try 'GetSlots -dd #'(#)followed by custom days.\033[0m")
        return 


def booked_schedule(result, email):
    """Getting the booker's booked schedule."""
    count = 0
    for event_data in result:
        if func_helper_to_get_attendees_email(event_data, email):
            # if help_to_get_open_slots(event_data) == False:
                count += 1
                table = Table()
                for key, value in event_data.items():
                    if key != "Event ID":
                        displaydata(key, value, table, count)
                console = Console()
                console.print(table)

    if count ==0:
        print(f"\033[1;31;10mNo events booked for {email} within {ui.command_line()[4]} days try, '-a GetSlots'.\033[0m")
    else:
        print("\033[1;36;10mYou can get slots with '-a GetSlots'.\033[0m")
        

def func_helper_to_get_attendees_email(event_data, email):
    """Checks for the booker's email."""
    for key, value in event_data.items():
        if key == "Event Attendee":
            if value == email:
                return True
    return False


def cancel_update_booking(result, email):
    """Cancels the booking done by the booker by updating the event."""
    event_ls1 = [""]
    count = 0

    for event_data in result:
        if func_helper_to_get_attendees_email(event_data, email):
            # if help_to_get_open_slots(event_data) == False:
                count += 1
                table = Table()
                for key, value in event_data.items():
                    if key == "Event ID":
                        event_ls1.append(value)
                    elif key != "summary":
                        displaydata(key, value, table, count)
                console = Console()
                console.print(table)
    if count >= 1:
        event_id_col = ui.menu_select(event_ls1[1:])
        return event_id_col
    if count == 0:
        print(f"\033[1;31;10mNo events to cancel for {email} within {ui.command_line()[4]} days.\033[0m")
    else:
        print("\033[1;36;10mYou can get more slots with '-a GetSlots'.\033[0m")
        return

            

