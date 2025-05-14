import time
from pymata4 import pymata4

# Low Level Functions
def get_inputs() -> dict:
    # Reads all inputs from the R-2R Ladder
    return {
        "PB1": True,
        "US1": False,
        "US2": False,
        "US3": True
    }

def handle_outputs():
    pass

# High Level Functions
def sleep(duration: float) -> float:
    """
    Function for assigning soft delay in between processes

    PARAMETERS:
    duration: Time in seconds of delay

    RETURN:
    endTime: The time at which the process should resume
    """
    return time.time() + duration

def change_light(lightSet: dict, lightPin: str):
    """
    Changes the active LED in the given light set to the one located at the desired pin

    PARAMETERS:
    lightSet (dict) -> What set of output pins will be modified
    lightPin (str) -> The name of the pin

    RETURNS:
    None
    """

    for light in lightSet: # Turns on selected pin, and turns off all other pins in the set
        if light == lightPin:
            lightSet[light] = 1
        else:
            lightSet[light] = 0
