from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
from backend.api import get_data, get_activity, get_appointments, get_procedures, get_ttm_activity, get_ytd_activity

def set_filter(at:Atri, selected_filter:str, flag:str):

    # Specialty
    at.specialty.custom.text = selected_filter

    # Extract data
    data = get_data(file_name='data.json')

    # Assign value to dropdown
    if flag == "page_request":
        at.specialty_dropdown.custom.values = list(data.keys())
        at.specialty_dropdown.custom.selectedValue = selected_filter

    # Activity line chart
    at.admissions.custom.data = get_activity(data[selected_filter])

    # Appointments
    app_data = get_data(file_name='app_data.json')
    at.appointments.custom.data = get_appointments(app_data[selected_filter])
    at.appointments.custom.options = {
        "Attended":{
            "fill":"#1E40AF"
        },
        "Not Attended":{
            "fill":"#FB923C"
        },
        "Canceled":{
            "fill":"#FACC15"
        }
    }
    at.appointments.custom.stacked = True
    
    # FCEs with procedures
    at.procedures.custom.data = get_procedures(data[selected_filter])
    at.procedures.custom.options = {
        "FCEs_with_Procedure":{
            "fill":"#7DD3FC"
        }
    }

    # TTM activity
    at.ttm_episodes.custom.cols = get_ttm_activity(data[selected_filter])[0]
    at.ttm_episodes.custom.rows = get_ttm_activity(data[selected_filter])[1]

    # YTD activity
    at.ytd_episodes.custom.cols = get_ytd_activity(data[selected_filter])[0]
    at.ytd_episodes.custom.rows = get_ytd_activity(data[selected_filter])[1]

def init_state(at: Atri):
    """
    This function is called every time "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the initial state of the app.
    """
    pass


def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    set_filter(at, selected_filter="100 general surgery service", flag="page_request")


def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    if at.specialty_dropdown.onChange:
        set_filter(at, selected_filter=at.specialty_dropdown.custom.selectedValue, flag="handle_event")