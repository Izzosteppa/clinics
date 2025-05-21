import argparse
import os.path
import re
import shutil
import sys
import textwrap
import time
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from sys import exit
import data_handling.data_modifier as dm
import data_handling.data_retriever as data_handler
from rich.progress import Progress
import itertools
import data_handling.pip_internal_data as internal_data
import data_handling.deleting_userdata as del_1
import logic_code.user_input as ui
from data_handling.data_modifier import extract_calendar_data_for_cal_ID
from simple_term_menu import TerminalMenu


def get_custom_date_event_creation_1():
    """Creates a custom date and validates the user input."""
    year, month, day = get_valid_date_input(ui.command_line()[2])
    hour, minute = valid_time_input(ui.command_line()[3])
    try:
        user_dt = datetime(int(year), int(month), int(day), int(hour), int(minute), 00)
        if (datetime.now()+ timedelta(minutes=10)) < user_dt:
            result = user_dt + timedelta(minutes=30)
            starting = str(user_dt).replace(" ", f"T")
            ending = str(result).replace(" ", f"T")
            return starting[:-3],ending[:-3]
        else:
            print("\033[1;31;10mInvalid date and time entered.\033[0m")
    except (ValueError,TypeError):
        print("\033[1;31;10mInvalid date and time entered.\033[0m")
    exit()


def automatic_copied():
    """
    Searches for a 'credentials.json' file within the user's home directory and copies it to a specific
    location ('.ccjhb16' folder in the user's home directory).
    """

    current_home_dir = os.path.join(os.path.expanduser("~"))
    with Progress() as progress:
        growth_1 = 0.03
        get_total = 0
        task1 = progress.add_task(
            "[yellow]Scanning local folders for 'creds.json'", total=1000
        )
        for r, d, f in os.walk(current_home_dir):
            for files in f:
                progress.update(task1, advance=growth_1)
                get_total += growth_1
                if files == "credentials.json":
                    file_to_copy = os.path.join(r, files)
                    destination_directory = os.path.join(
                        os.path.expanduser("~"), ".ccjhb16"
                    )
                    if (
                        file_to_copy != destination_directory
                        and file_to_copy.find("Trash") == -1
                    ):
                        progress.update(task1, advance=1000 - get_total)
                        time.sleep(1)
                        progress.update(task1, visible=False)
                        try:
                            shutil.copy(file_to_copy, destination_directory)
                            print(f"\033[1;36;10mAutomatically copied {file_to_copy} to {destination_directory}\033[0m")
                            return
                        except shutil.SameFileError:
                            return


def resource_path(relative_path):
    """
    Gets the absolute path to a resource, ensuring compatibility both in development and in a PyInstaller
    bundled application. It also ensures the existence of a specific directory ('.ccjhb16') in the user's
    home directory and attempts to automatically copy 'credentials.json' into it if not present.
    """
    create_app_dir = os.path.join(os.path.expanduser("~"), ".ccjhb16")
    if not os.path.exists(create_app_dir):
        os.makedirs(create_app_dir)
        print(f"\033[1;36;10mPlease move your credentials.json to '{create_app_dir}'\033[0m")
        automatic_copied()
        exit()
    creds_check1 = os.path.join(os.path.expanduser("~"), ".ccjhb16", relative_path)
    if relative_path == "credentials.json":
        if not os.path.isfile(creds_check1):
            print(f"\033[1;36;10mPlease move your credentials.json to '{create_app_dir}'\033[0m")
            automatic_copied()
            exit()
    return creds_check1


def cal_to_verfiy(service):
    """Verifies the presence of a calendar containing the word 'clinic' in its ID within the user's Google Calendar."""

    data_of_cal_ls = extract_calendar_data_for_cal_ID(
        service.calendarList().list().execute()
    )[0]
    cal_ID = []
    sub_str_2 = "clinic"
    for data in data_of_cal_ls:
        keys_r = data.keys()
        if str(keys_r).find(sub_str_2) != -1:
            values_r = data.values()
            cal_ID.append(list(values_r)[0])
    if len(cal_ID) == 1:
        return cal_ID[0]
    elif len(cal_ID) >1:
        print("\033[1;31;10mFound more than 1 calendar containing the word 'clinic'.\033[0m")
        print("\033[1;31;10mPlease rename or remove other calendars and leave only one calender containing the word 'clinic'.\033[0m")
        exit()
    else:
        print("\033[1;31;10mNo calendar found containing the word 'clinic' please ensure you use clinic in your group calendar.\033[0m")
        exit()


def command_line_help():
    """
    This function provides detailed descriptions of each command line option available in the application,
    including volunteer and booker commands, along with examples of their usage.
    """
    return textwrap.dedent(
        """\

            \033[1;35;10m--VOLUNTEER COMMANDS--
        --OPTIONS--                     
        \033[1;36;10mViewSlots - \033[1;34;10mView your open slots.
        \033[1;36;10mAddSlot - \033[1;34;10mAdding a slot.
        \033[1;36;10mBookedSlots - \033[1;34;10mView your booked slots.
        \033[1;36;10mCancelEmptySlot -\033[1;34;10mCancellation of an empty slot.
                           
            \033[1;35;10m--BOOKER COMMANDS--
        \033[1;36;10mViewCal - \033[1;34;10mView your personal events.
        \033[1;36;10mGetSlots - \033[1;34;10mViewing available slots.
        \033[1;36;10mCancelBookedSlot - \033[1;34;10mCanceling your booked slot.
        \033[1;36;10mViewBookedSlots - \033[1;34;10mView your booked slots.
        \033[1;36;10mDocs - \033[1;34;10mSee all valid volunteers.
        \033[1;36;10mExpCal - \033[1;34;10mExport all Slots in iCal format so it can be imported into a calendar application. (<custom iCal_link>)
        
                      
            \033[1;35;10m--Example usage--
        \033[1;36;10m'--action GetSlots (optional):-dd <custom days>'                
        \033[1;36;10m'--action ViewCal -loc WTC_Campus'                
        \033[1;36;10m'--action AddSlot --date ... --time ... -loc WTC_Campus'                
        \033[1;36;10m'--action ExpCal -url <custom iCal_link>'             
                            """
    )


def command_line():
    """
    This function uses argparse to define and parse command line arguments. It supports various commands
    and options, including login, action specification, and others.
    """

    parser = argparse.ArgumentParser(
        description="\033[1;36;10mCommand line arguments.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--username",
        "-u",
        metavar="",
        help="\033[1;33;10mTo log in, use -u followed by your username e.g '-u jay023'\033[3;36;10m",
    )
    parser.add_argument(
        "--action",
        "-a",
        metavar="",
        choices=[
            "ViewSlots",
            "BookedSlots",
            "CancelEmptySlot",
            "AddSlot",
            "GetSlots",
            "CancelBookedSlot",
            "ViewBookedSlots",
            "ViewCal",
            "ExpCal",
            "Docs",
        ],
        help=command_line_help(),
    )


    parser.add_argument(
        "--location",
        "-loc",
        metavar="",
        choices=[
            "WTC_EWC",
            "WTC_DBN",
            "WTC_CPT",
            "WTC_CJC",
        ], default= "WTC_JHB", help="WTC_EWC, WTC_DBN, WTC_CJC, WTC_CPT (Default:WTC_JHB)"
    )

    parser.add_argument(
        "--date",
        metavar="'YYYY-MM-DD'",
        required="AddSlot" in sys.argv,
        help="\033[1;32;10mAdd Date\033[1;36;10m",
    )


    parser.add_argument(
        "--custom_url",
        "-url",
        metavar="",
        default="cc16",
        help="\033[1;32;10mInput custom iCal URL.'\033[1;36;10m",
)
    
    parser.add_argument(
        "--time", metavar="'HH:MM'", required="AddSlot" in sys.argv, help="\033[1;32;10mAdd Time\033[1;36;10m"
    )
    parser.add_argument(
        "--custom_days",
        "-dd",
        metavar="",
        type=int,
        default=7,
        help="\033[1;32;10mConfigure the number of days of events data to view e.g '-dd 31'\033[1;36;10m",
    )
    parser.add_argument("--Logout", metavar="'jay023'", help="\033[1;32;10mLogout of the system")
    args = parser.parse_args()

    if args.username != None:
        result = ui.get_username(args.username)
    else:
        result = internal_data.events_writer("no_username","user_data.pkl")
    if args.action:
        return result, args.action, args.date, args.time, args.custom_days,args.location,args.custom_url
    elif args.Logout:
        return False
    elif args.action == None:
        return result, "Login"


def get_booker_description():
    """
    Prompts the user to enter a description for an event, ensuring it's longer than 6 characters.
    """
    while True:
        get_input = input("Enter a description longer than 6 characters: ")
        if len(get_input) > 6:
            return get_input


def get_valid_date_input(date_str):
    """
    Validates and parses a date string input by the user, ensuring it follows the 'YYYY-MM-DD' format.
    """

    new_list = []
    if len(date_str) == 10 and "-" in date_str:
        date_list = date_str.split("-")
        new_list.append(date_list[0])
        for i in date_list[1:]:
            if i.isdigit():
                replaced_value = i.lstrip("0")
                new_list.append(replaced_value)
            else:
                print(
                    "\033[1;31;10mInvalid date format. Please enter a date in the format yyyy-mm-dd.\033[0m"
                )
                exit()
        return new_list[0], new_list[1], new_list[2]
    print("\033[1;31;10mInvalid date format. Please enter a date in the format yyyy-mm-dd.\033[0m")
    exit()


def get_username(username):
    """Validates the format of a username input by the user."""

    if (
        len(username) > 5
        and username[-3:].isdigit()
        and username[0:2].isalpha()
        and "@" not in username
    ):
        return f"{username.lower().strip()}@student.wethinkcode.co.za"
    print("\033[1;31;10mInvalid username. \033[0m")
    exit()


def collecting_events(service,emails,days,location):
    """Collects events data for a specific email."""

    primary_cal_info = dm.extract_event_data(
        data_handler.get_events_data_from_api(
            emails,
            service.events().list,
            f"Checking updates on {emails[:-26]} calendar..",
            days
        ), location
    )
    return primary_cal_info


def error_handling_for_primary_cal(service,stu_email,days,location):
    """Handles errors for primary calendar events."""


    try:
        events_primary_data = internal_data.events_writer(collecting_events(service,stu_email,days,location), "primary_events_info.pkl")
        internal_data.events_writer(stu_email, "user_data.pkl")
    except HttpError as err:
        if err.resp.status == 404:
            time.sleep(2)
            del_1.delete_files(ui.resource_path("user_data.pkl"), "file2", "file3", 1)
            print(f"\033[1;31;10mInvalid WeThinkCode_ student username use e.g'jay023'\033[0m")
        else:
            print(f"\033[0;37;10mPlease give us permission to read your personal events\033[0m")
        exit()
    return events_primary_data

def helper_to_get_evnts_ids(service,cal_ID,list_cc_cal):
    """Helper function to get event IDs. Gets into events and compares code clinics and primary calendars, then pairs up the same events."""

    ids = []
    acl = service.acl().list(calendarId=cal_ID).execute()
    email_list = [
        entry["scope"]["value"]
        for entry in acl["items"]
        if entry["scope"]["type"] == "user"
    ]
    for i in email_list[1:]:
        try:
            primary_cal_info = collecting_events(service,i,command_line()[4],command_line()[5])
        except HttpError as err:
            print(f"\033[0;37;10mPlease ask {i[:-26]} to give you permission to modify their personal events\033[0m")
            primary_cal_info = []
        if len(primary_cal_info) >= 1:
            for p in primary_cal_info:
                for cc in list_cc_cal:
                    a_1=dict(itertools.islice(p.items(), 1, 10))
                    a_2=dict(itertools.islice(cc.items(), 1, 10))
                    if a_1 == a_2:
                        event_id_cc = cc["Event ID"]
                        event_id_p_cc = p["Event ID"]
                        creator_email = cc["Event Creator Email"]
                        ids.append((event_id_cc, event_id_p_cc, creator_email))
    return ids


def valid_doc(service, cal_ID):
    """Prints valid volunteer's with access to a calendar."""

    acl = service.acl().list(calendarId=cal_ID).execute()
    email_list = [
        entry["scope"]["value"]
        for entry in acl["items"]
        if entry["scope"]["type"] == "user"
    ]
    for i in email_list[1:]:
        print(i)
    

def valid_time_input(time_input):
    """Validates time input."""

    if re.match(r"^[0-2][0-9]:[0-5][0-9]$", time_input):
        return time_input.split(":")
    else:
        print("\033[1;31;10mInvalid time format. Please enter a valid time.\033[0m")
        exit()

def validate_volunteer(service,user_email):
    """Verifys the users token to """
    token_email = extract_calendar_data_for_cal_ID(
        service.calendarList().list().execute())[1]
    if user_email == token_email:
        return True
    else:
        print(f"\033[1;31;10mThe username from your token is not the same as your login username: {user_email[:-26]}\033[0m")
        print(f"\033[1;33;10mPlease login using '-u {token_email[:-26]}' to add a slot.\033[0m")
        exit()



def clinician_validator(service, user_email, cal_ID):
    """Validates clinician access to a calendar."""

    acl = service.acl().list(calendarId=cal_ID).execute()
    wild_card = "2023.cohort@wethinkcode.co.za"
    email_list = [
        entry["scope"]["value"]
        for entry in acl["items"]
        if entry["scope"]["type"] == "user"
    ]
    if user_email in email_list or wild_card in email_list:
        return True
    return False


def menu_select(events_list):
    """Displays a menu for selecting events containing the event IDs."""
    
    other_list = []
    for i in range(1, len(events_list) + 1):
        other_list.append("Event " + str(i))
    terminal_menu = TerminalMenu(other_list, title = "Please select an event by using arrow keys(Up/Down)")
    menu_entry_index = terminal_menu.show()
    return events_list[menu_entry_index]