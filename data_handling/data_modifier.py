
def extract_event_data(data_list, campus):
    """Gets event data from data_retriever and refines it into a dictionary."""
    extracted_data = []

    for event in data_list:
        event_id = event["id"]
        event_summary = event.get("summary", "No Title")
        event_description = event.get("description", "No Description")
        event_location = event.get("location",campus)
        event_start_time = event["start"].get("dateTime",str(event["start"].get("date"))+"T00:00:00+02:00")
        event_end_time = event["end"].get("dateTime", str(event["end"].get("date"))+"T23:59:00+02:00")
        event_creator_email = event["creator"]["email"]

        try:
            event_attendees_email = event["attendees"][0]["email"]
            if event_creator_email == event_attendees_email:
                event_attendees_email = event["attendees"][1]["email"]
        except (KeyError, IndexError):
            event_attendees_email = "No Attendees"

        event_data = {
            "Event ID": event_id,
            "Event Summary": event_summary,
            "Event Description": event_description,
            "Event Location": event_location,
            "Event Start Time": event_start_time[:-9],
            "Event End Time": event_end_time[:-9],
            "Event Creator Email": event_creator_email,
            "Event Attendee": event_attendees_email,
        }

        extracted_data.append(event_data)

    return extracted_data


def extract_calendar_data_for_cal_ID(calendar_data):
    """Extracts calendar data."""
    extracted_data = []
    for calendar_entry in calendar_data["items"]:
        calendar_id = calendar_entry["id"]
        calendar_summary = calendar_entry.get("summary", "").lower()
        calendar_data1 = {calendar_summary: calendar_id}
        extracted_data.append(calendar_data1)
        if calendar_entry.get('primary'):
            real_user_email = calendar_entry.get('id')
    return extracted_data,real_user_email
