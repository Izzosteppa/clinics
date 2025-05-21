import clinician_booker_options.booker_options as book_opt
import clinician_booker_options.clinician_options as doc_opt
import clinician_booker_options.view_cal as vc
import logic_code.event_creatie_update_del as event_handler
import logic_code.user_input as ui
from data_handling.ical_exporter import download_cal_to_ical


def home_page(service, cal_ID, result, email):
    """Checks the user's choice of function."""
    choice1 = ui.command_line()[1]
    if ui.clinician_validator(service, email, cal_ID):
        if choice1 == "ViewSlots":
            doc_opt.view_your_schedule_open(result, email)
        elif choice1 == "BookedSlots":
            doc_opt.valid_appointments(result, email)
        elif choice1 == "CancelEmptySlot":
            primary_cal_info = ui.helper_to_get_evnts_ids(service,cal_ID,result)
            event_ID = doc_opt.cancel_slot(result, email)
            if event_ID != None:
                event_handler.delete_event(service, event_ID, cal_ID,primary_cal_info)
                print("\033[1;32;10mYou have successfully cancelled a slot.\033[0m")
        elif choice1 == "AddSlot":
            ui.validate_volunteer(service,email)
            print(
                event_handler.creation_of_event(
                    service, cal_ID, doc_opt.adding_slot_validator(result)
                )
            )
    if (
        ui.clinician_validator(service, email, cal_ID)
        or ui.clinician_validator(service, email, cal_ID) == False
    ):
        if choice1 == "ViewBookedSlots":
            book_opt.booked_schedule(result, email)
        elif choice1 == "ViewCal":
            pry_events_data = ui.error_handling_for_primary_cal(service,email,ui.command_line()[4],"WTC")
            vc.view_your_schedule(pry_events_data,email)
        elif choice1 == "GetSlots":
            primary_cal_info = ui.helper_to_get_evnts_ids(service,cal_ID,result)
            event_ID = book_opt.getting_a_slot(result, email)
            if event_ID != None:
                event_handler.update_event(service, event_ID, cal_ID, ui.get_booker_description(), email, primary_cal_info)
                print("\033[1;32;10mYou have successfully booked a slot.\033[0m")
        elif choice1 == "CancelBookedSlot":
            primary_cal_info = ui.helper_to_get_evnts_ids(service,cal_ID,result)
            event_ID = book_opt.cancel_update_booking(result, email)
            if event_ID != None:
                event_handler.cancel_booked_slot(service, event_ID, cal_ID,primary_cal_info)
                print("\033[1;32;10mYou have successfully cancelled a slot.\033[0m")
        elif choice1 == "ExpCal":
            download_cal_to_ical(ui.command_line()[6])
        elif choice1 == "Docs":
            ui.valid_doc(service, cal_ID)
