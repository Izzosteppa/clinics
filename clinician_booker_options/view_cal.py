from rich.console import Console
from rich.table import Table
import itertools

from data_handling.data_visualizer import displaydata


def view_your_schedule(result, email):
    """Views primary calendar."""
    count = 0

    for index,event_data in enumerate(result):
        table = Table()
        previous_event_in_list=dict(itertools.islice(event_data.items(), 1, 10))
        current_event_in_list=dict(itertools.islice(result[index-1].items(), 1, 10))
        if previous_event_in_list != current_event_in_list:
            count += 1 #Counting only if there are no duplicate events
            for key, value in event_data.items():
                if key != "Event Description":
                    if key != "Event ID":
                        displaydata(key, value, table, count)
        console = Console()
        console.print(table)
    if count == 0:
        print(f"\033[1;31;10mNo events for {email}.\033[0m")
