import time
from pymata4 import pymata4


regOrder1 = [ # The order in which we write to each pin in the register
    "TL1 R", "TL1 Y", "TL1 G",
    "TL2 R", "TL2 Y", "TL2 G",
    "TL3 R", "TL3 G"
]
regOrder2 = [
    "TL4 R", "TL4 Y", "TL4 G",
    "TL5 R", "TL5 Y", "TL5 G",
    "PL1 R", "PL1 G"
]
regOrder3 = [
    "PA1", "WL WL1", "WL WL2",
    "FL", "US1", "US2",
    "US3", "None"
]

# Low Level Functions (Works directly with the Arduino)
def get_inputs(debug: bool, board: pymata4.Pymata4 = None) -> dict:
    """
    A low level handler for reading and filtering all inputs from sensors and buttons across the Arduino

    PARAMETERS:
    debug -> True if we want to just use test values for inputs
    board = None -> The Arduino we will be reading from. If None, we are just debugging our code

    RETURNS:
    inputs (dict) -> A dictionary containing all read input values in boolean form
    """
    # PB1 handling
    if not debug:
        pb = board.analog_read(0)[0]
        pb1 = True if pb < 600 else False
    else:
        pb1 = False
    
    if not debug: # Checking values of ultrasonic sensors
        us1 = True if 2 <= board.sonar_read(9)[0] <= 100 else False
        us2 = True if 2 <= board.sonar_read(11)[0] <= 100 else False
        us3 = True if 2 <= board.sonar_read(13)[0] <= 100 else False
    else:
        us3 = False
        us2 = False
        us1 = True

    
    return {
        "PB1": pb1,
        "US1": us1,
        "US2": us2,
        "US3": us3,
        "DS1": True
    }

def handle_outputs(board: pymata4.Pymata4, register1: dict, register2: dict, register3: dict, pinSet: dict):
    """
    Sends output to shift registers for output pin handling

    PARAMETERS:
    board -> The Arduino board to be written to
    register1, register2, register3 -> Dictionaries containing the pin data we want to send to our shift registers
    pinSet -> A dictionary outlining which Arduino output pin is assigned to each shift register input
    """

    write_reg(board, pinSet, register1, register2, register3)

def write_reg(board: pymata4.Pymata4, pinSet: dict, reg1: dict, reg2: dict, reg3: dict):
    """
    Low level function that writes all output pin data to shift registers

    PARAMETERS:
    board -> The Arduino board to be written to
    pinSet -> A dictionary outlining which Arduino output pin is assigned to each shift register input
    reg1, reg2, reg3 -> Dictionaries containing the pin data we want to send to our shift registers
    """
    # Individual data pins for each register (basically sending 1 or 0)
    dataReg1 = pinSet["outputs"]["SER1"]
    dataReg2 = pinSet["outputs"]["SER2"]
    dataReg3 = pinSet["outputs"]["SER3"]

    # Pins that control all three registers
    clockPin = pinSet["outputs"]["SRCLK"]
    latchPin = pinSet["outputs"]["RCLK"]

    board.digital_write(latchPin, 0)

    reg1 = flatten_dict(reg1) # Removes all group names in each dict (like "TL1", which doesn't refer to just one pin)
    reg2 = flatten_dict(reg2)
    reg3 = flatten_dict(reg3)
    
    bits1 = [reg1.get(k, 0) for k in regOrder1]
    bits1 = list(reversed(bits1))  # Shift Registers take inputs in reversed order

    bits2 = [reg2.get(k, 0) for k in regOrder2]
    bits2 = list(reversed(bits2))

    bits3 = [reg3.get(k, 0) for k in regOrder3]
    bits3 = list(reversed(bits3))

    # Shift out bits
    for bit in range(8):
        # This is where we write the current pin state to each shift register
        board.digital_write(dataReg1, bits1[bit])
        board.digital_write(dataReg2, bits2[bit])
        board.digital_write(dataReg3, bits3[bit])
        
        # Tells all shift registers to move onto next pin
        board.digital_write(clockPin, 1)
        time.sleep(0.01)
        board.digital_write(clockPin, 0)

    # Latch the outputs
    board.digital_write(latchPin, 1)
    time.sleep(0.0001)
    board.digital_write(latchPin, 0)

# High Level Functions (Handles logic within the program and interacts with registers through dictionaries)
def sleep(duration: float) -> float:
    """
    Function for assigning soft delay in between processes. (Important to note that it doesn't actually pause anything on its own)

    PARAMETERS:
    duration: Time in seconds of delay

    RETURN:
    endTime: The time at which the process should resume
    """
    return time.time() + duration

def flatten_dict(oldDict: dict) -> dict:
    """
    Turns a dict with nested dicts into a single dict

    e.g. SER = {"dict": {"item1": 0, "item2": 1}}
    SER =  {"item1": 0, "item2": 1}

    PARAMETERS:
    oldDict -> The dictionary to be 'flattened'

    RETURNS:
    newDict (dict) -> The flattened dictionary
    """
    flat = {}
    for key, value in oldDict.items():
        if isinstance(value, dict):
            # Calls itself to organise nested dicts
            nested_dict = flatten_dict(value)

            for idx, val in nested_dict.items():
                flat[f"{key} {idx}"] = val
        else:
            flat[key] = value
    return flat

def change_light(lightSet: dict, lightPin: str) -> None:
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

def pin_on(lightSet, lightPin) -> None:
    """
    Turns desired pin on

    PARAMETERS:
    lightSet -> The dict containing the pin to be switched off
    lightPin -> Name of the pin to be switched

    RETURNS:
    None
    """
    lightSet[lightPin] = 1

def pin_off(lightSet: dict, lightPin: str) -> None:
    """
    Turns desired pin off

    PARAMETERS:
    lightSet -> The dict containing the pin to be switched off
    lightPin -> Name of the pin to be switched

    RETURNS:
    None
    """
    lightSet[lightPin] = 0

def flash_light(lightSet: dict, lightPin: str, interval: int, startTime=0, phase=0, clock=0.0) -> dict:
    """
    PARAMETERS:
    lightSet -> The set of output LEDs to be modified
    lightPin -> The LED within lightSet to be flashed on and off
    interval -> The amount of time in s that the Arduino will wait between each change in state
    
    These parameters have default values. The first time you call this function leave these blank so the program knows you only just started flashing the lights

    startTime (int) = 0 -> Time that the function was first called
    phase (int) = 0 -> Current state of the function
    clock (float) = 0.0 -> Time when function next needs to change state

    RETURNS:
    flashingState (dict) -> A dictionary containing the above three values so that the function can pick up where it left off last loop
    """
    
    if startTime == 0:
        startTime = time.time()
        clock = sleep(interval/2)


    match phase:
        case 0:

            if clock <= time.time():
                clock = sleep(interval/2)
                phase = 1
            else:
                lightSet[lightPin] = 1
                    
        case 1:

            if clock <= time.time():
                clock = sleep(interval/2)
                phase = 0
            else:
                lightSet[lightPin] = 0
    
    return {
        "start": startTime,
        "phase": phase,
        "clock": clock
    }