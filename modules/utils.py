import time
from pymata4 import pymata4


regOrder1 = [ # The order in which we write to each pin in the register
    "TL1 R", "TL1 Y", "TL1 G",
    "TL2 R", "TL2 Y", "TL2 G",
    "TL3 R", "TL3 Y", "TL3 G"
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

# Low Level Functions
def get_inputs(debug: bool, board: pymata4.Pymata4 = None) -> dict:
    # Debugging for Subsystem 2
    if not debug:
        pb = board.analog_read(0)[0]
        pb1 = True if pb < 600 else False
    else:
        pb1 = True
    
    if not debug:
        # us2 = True if board.digital_read(12)[0] == 0 else False # Debugging for subsystem 2

        us3 = True if 2 <= board.sonar_read(9)[0] <= 100 else False # Debugging for subsystem 4
    else:
        us3 = False
        us1 = True

    us2 = False
    
    return {
        "PB1": pb1,
        "US1": False,
        "US2": False,
        "US3": True
    }

def handle_outputs(board: pymata4.Pymata4, register1: dict, register2: dict, register3: dict, pinSet: dict):
    """ board.digital_write(4, register1["TL3"]["R"]) # TL3 Red
    #board.digital_write(5, register1["TL3"]["Y"]) # TL
    board.digital_write(5, register1["TL3"]["G"]) # TL3 Green """

    """ board.digital_write(6, register["PL1"]["G"])
    board.digital_write(7, register["PL1"]["R"]) """

    """ board.digital_write(10, register3["WL"]["WL1"]) # WL 1
    board.digital_write(11, register3["WL"]["WL2"]) # WL 2 """


    write_reg(board, pinSet, register1, register2, register3)

def test_outputs(board: pymata4.Pymata4, register):
    board.digital_write(2, register["TL4"]["R"])
    board.digital_write(3, register["TL4"]["Y"])
    board.digital_write(4, register["TL4"]["G"])

def pulse(board: pymata4.Pymata4, pin: int, delay=0.001):
    board.digital_write(pin, 1)
    time.sleep(delay)
    board.digital_write(pin, 0)
    time.sleep(delay)

def clear_register(board: pymata4.Pymata4, clearPin: int):
    board.digital_write(clearPin, 0)  # active LOW
    time.sleep(0.01)
    board.digital_write(clearPin, 1)  # back to normal
    time.sleep(0.01)

def write_reg(board: pymata4.Pymata4, pinSet: dict, reg1: dict, reg2: dict, reg3: dict):

    # Individual data pins for each register (basically sending 1 or 0)
    dataReg1 = pinSet["outputs"]["SER1"]
    dataReg2 = pinSet["outputs"]["SER2"]
    dataReg3 = pinSet["outputs"]["SER3"]

    # Pins that control all three registers
    CLOCK_PIN = pinSet["outputs"]["SRCLK"]
    LATCH_PIN = pinSet["outputs"]["RCLK"]

    board.digital_write(LATCH_PIN, 0)

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
        board.digital_write(CLOCK_PIN, 1)
        time.sleep(0.01)
        board.digital_write(CLOCK_PIN, 0)

    # Latch the outputs
    board.digital_write(LATCH_PIN, 1)
    time.sleep(0.0001)
    board.digital_write(LATCH_PIN, 0)



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

def flatten_dict(old_dict: dict) -> dict:
    """
    Turns a dict with nested dicts into a single dict

    e.g. SER = {"dict": {"item1": 0, "item2": 1}}
    SER =  {"item1": 0, "item2": 1}
    """
    flat = {}
    for key, value in old_dict.items():
        if isinstance(value, dict):
            # Calls itself to organise nested dicts
            nested_dict = flatten_dict(value)

            for idx, val in nested_dict.items():
                flat[f"{key} {idx}"] = val
        else:
            flat[key] = value
    return flat

def save_reg(*regs):
    """
    A function that saves the state of a dictionary with other nested dicts

    This allows us to store the old values stored on the shift registers and the new values at the same time
    """
    savedRegs = []
    for reg in regs: # Each shiftRegister dictionary
        savedReg = {}
        for pinset in reg: # Checks the pinset variables: like TL4 = {} or FL1 = 0
            if type(reg[pinset]) is dict: # When pinset is a nested dict like TL4
                pins = {}
                for pin in reg[pinset]:
                    pins[pin] = reg[pinset][pin] 
                
                savedReg[pinset] = pins
            else: # When pinset is a single pin like FL1
                savedReg[pinset] = reg[pinset]
        
        savedRegs.append(savedReg)
    
    return savedRegs

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

def kill_lights(lightSet):
    for light in lightSet:
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