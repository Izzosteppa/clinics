import os.path

from sys import exit, argv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import data_handling.data_modifier as dm
import data_handling.data_retriever as data_handler
import data_handling.deleting_userdata as erase
import data_handling.pip_internal_data as internal_data
import logic_code.home as user_game
import logic_code.user_input as ui

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    """The main file to run the whole program. Shows usage of the Google Calendar API."""

    erase.delete_files(
        ui.resource_path("user_data.pkl"),
        ui.resource_path("token.json"),
        ui.resource_path("events_data.pkl"),
    )
    if len(argv) == 1 or (
        os.path.exists(ui.resource_path("user_data.pkl")) == False
        and "--username" not in argv
    ):
        if "-u" not in argv:
            argv.append("-h")
            print("\033[1;31;10mPlease log in first.\033[0m")

    creds = None
    if os.path.exists(ui.resource_path("token.json")):
        creds = Credentials.from_authorized_user_file(
            ui.resource_path("token.json"), SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ui.resource_path("credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(ui.resource_path("token.json"), "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        cal_ID = ui.cal_to_verfiy(service)
        if ui.command_line() == False:
            erase.delete_files(
                ui.resource_path("user_data.pkl"),
                ui.resource_path("token.json"),
                ui.resource_path("events_data.pkl"),
                1,
            )
            print("\033[1;32;10mSuccessfully logged out\033[0m")
            exit()
        stu_email = ui.command_line()[0]
        if ui.command_line()[1] == "Login":
            ui.error_handling_for_primary_cal(service,stu_email,3,"WTC")
            print(f"\033[1;32;10mSuccessfully logged in as {stu_email}.\033[0m")
            if ui.clinician_validator(service, stu_email, cal_ID) == False:
                print("\033[1;36;10mRemember you are only allowed to do Booker Options\033[0m")
            exit()
            
        event_raw_data = data_handler.get_events_data_from_api(
            cal_ID,
            service.events().list,
            "Checking updates on code_clinics_calendar..",
            ui.command_line()[4]
        )
        result = internal_data.events_writer(dm.extract_event_data(event_raw_data, ui.command_line()[5]),"events_data.pkl")
        if ("-u" not in argv):
            if ("--username" not in argv):
                user_game.home_page(service, cal_ID, result, stu_email)
        else:
            print("Please login first then use '-a' ...")

    except (HttpError, NameError) as error:
        if error.resp.status == 403:
            print("\033[1;32;10mYou don't have the rights to change events on the Google Calendar.\033[0m")
        else:
            print(f"\033[1;31;10mAn error occurred: {error}\033[0m")


if __name__ == "__main__":
    main()
