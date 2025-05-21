import datetime
import random

from rich.progress import Progress


def convert_date_to_iso(period_of_days):
    """Converts date to iso format and returns the date and the end period of the date."""
    date_to_replace = "0001-01-01T00:00:00-00:00"
    date_now = datetime.datetime.now().date()
    end_period = (datetime.datetime.now() + datetime.timedelta(period_of_days)).date()
    final_end_period = date_to_replace.replace("0001-01-01", str(end_period))
    stating_date = date_to_replace.replace("0001-01-01", str(date_now))
    stating_time = stating_date.replace("00:00:00-00:00", str(datetime.datetime.now().time())+"Z")
    return stating_time, final_end_period


def get_events_data_from_api(cal_ID, get_data,message,period_of_days=7):
    """Gets the events from the api and returns the data."""
    with Progress() as progress:
        growth_1 = random.randint(10, 70)
        task1 = progress.add_task("[yellow]"+message, total=100)
        progress.update(task1, advance=growth_1)
        events_data = (
            get_data(
                calendarId=cal_ID,
                orderBy="startTime",
                timeMin=convert_date_to_iso(period_of_days)[0],
                timeMax=convert_date_to_iso(period_of_days)[1],
                singleEvents=True,
                alwaysIncludeEmail=True,
                showDeleted=None,
            )
            .execute()
            .get("items")
        )
        progress.update(task1, advance=100 - growth_1)
        return events_data
