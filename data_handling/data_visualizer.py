

def displaydata(keys, values, table, cont):
    """ Displays the data in a table format."""
    if keys == "Event Summary":
        table.add_column(f"{cont}.Event details")
        table.add_column("Event info", justify="left", )
    elif keys in ["Event Start Time", "Event End Time"]:
        stime = values.split("T")
        values = f"{stime[0]}[bold]🌐{stime[1]}🌐"
    table.add_row(keys, values)
