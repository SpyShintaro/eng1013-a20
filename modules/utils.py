import time
from pymata4 import pymata4

# Low Level Functions
def get_inputs(debug: bool, board: pymata4.Pymata4 = None) -> dict:
    if not debug:
        pb1 = True if board.digital_read(12)[0] == 0 else False
    else:
        pb1 = True
    
    return {
        "PB1": pb1,
        "US1": False,
        "US2": False,
        "US3": True
    }

def handle_outputs(board: pymata4.Pymata4, register: dict):
    board.digital_write(2, register["TL4"]["R"])
    board.digital_write(3, register["TL4"]["Y"])
    board.digital_write(4, register["TL4"]["G"])

    board.digital_write(6, register["PL1"]["G"])
    board.digital_write(7, register["PL1"]["R"])

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

def flash_light(lightSet: dict, lightPin: str, interval: int, startTime=0, phase=0, clock=0.0):
    """
    PARAMATERS:
    lightSet -> The set of output LEDs to be modified
    lightPin -> The LED within lightSet to be flashed on and off
    interval -> The amount of time in s that the Arduino will wait between each change in state
    
    These parameters have default values. The first time you call this function leave these blank so the program knows you only just started flashing the lights

    startTime (int) = 0 -> Time that the function was first called
    phase (int) = 0 -> Current state of the function
    clock (float) = 0.0 -> Time when function next needs to change state

    RETURNS:
    None
    """
    
    if startTime == 0:
        startTime = time.time()
        clock = sleep(interval)


    match phase:
        case 0:

            if clock <= time.time():
                clock = sleep(interval)
                phase = 1
            else:
                lightSet[lightPin] = 1
                    
        case 1:

            if clock <= time.time():
                clock = sleep(interval)
                phase = 0
            else:
                lightSet[lightPin] = 0
    
    return {
        "start": startTime,
        "phase": phase,
        "clock": clock
    }