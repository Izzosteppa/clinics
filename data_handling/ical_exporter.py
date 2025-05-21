import requests


def iCal_input(url):
    """Gets the user input for the calendar export."""
    ical_url = "https://calendar.google.com/calendar/ical/c_339b5fd0ec89e5bf92dd35f8037120ddd7603869b58669e4b66c538341d22645%40group.calendar.google.com/private-c075adbd405cab7454875d06b899c266/basic.ics"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        default_response = requests.get(ical_url)
        print("\033[1;31;10mPlease specify a valid URL.\033[0m")
        print("\033[0;37;10mWe'll download default calendar.\033[0m")
        return default_response.text


def download_cal_to_ical(ical_url):
    """Export the bookings in iCal file format so that it can be
    imported into a desktop calendar application."""
   
    ical_content = iCal_input(ical_url)
    with open("Code_clinics_1.ics", "w") as file:
        file.write(ical_content)
    print("\033[1;32;10mCode_clinics successfully exported  in iCal format. Ready for import.\033[0m")




