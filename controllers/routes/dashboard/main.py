from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
from backend.api import apply_dropdown_values, set_filter

def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    # describe column headers and the data type
    pass


def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    apply_dropdown_values(at)
    pass


def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    if at.Dropdown1.onChange:
        set_filter(at, at.Dropdown1.custom.selectedValue)

    pass