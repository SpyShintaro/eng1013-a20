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

def flash_light(lightSet: dict, lightPin: str, interval: int, length: int, startTime=0, timeCheck=0, phase=0, clock=0):
    """
    PARAMATERS:
    lightSet -> The set of output LEDs to be modified
    lightPin -> The LED within lightSet to be flashed on and off
    interval -> The amount of time in ms that the Arduino will wait between each change in state
    length -> The time in seconds that the function will run

    RETURNS:
    None
    """

    for light in lightSet: # Turns off all LEDs in light set
        lightSet[light] = 0
    
    if startTime == 0:
        startTime = time.time()


    if time.time() - startTime <= length: # Checks to make sure the function hasn't been running longer than the given length
        match phase:
            case 0:
                if clock <= time.time():
                    lightSet[lightPin] = 1
                    clock = sleep(interval/1000)
                    phase = 1
                
            
            case 1:
                if clock <= time.time():
                    lightSet[lightPin] = 0
                    clock = sleep(interval / 1000)
                    phase = 0
        
        return {
            "start": startTime,
            "time": timeCheck,
            "phase": phase,
            "clock": clock
        }