"""
Tunnel Ave Subsystem - Traffic Control Subsystem 2

Author: Jake
Original Version Date: 14/04/2025
Version Number: 1.0
"""
import time
from pymata4 import pymata4

# Input Pins
inPB1 = 2

# Output Pins
outTL4 = { # Grouped LEDs for the traffic light
    "G": 8,
    "Y": 7,
    "R": 6
}

outPL1 = { # Grouped LEDs for the pedestrian lights
    "G": 9,
    "R": 10
}

interval = 200 # Half the time interval of each flash of the light

def main():
    """
    Primary Subsystem Loop

    PARAMETERS:
    None

    RETURNS:
    None
    """

    # Initialise normal pins
    change_light(outTL4, "G")
    change_light(outPL1, "R")

    while True:
        try:
            pbState = get_inputs()

            if pbState:
                pb_pressed()
        except KeyboardInterrupt as e: # Keyboard interrupt to kill all communication with Arduino
            print('Ending Program')
            board.shutdown()
            raise e


def setup():
    """
    Configures all of the pin modes used in the program (USE IT !!!!)

    PARAMETERS:
    None

    RETURNS:
    None
    """
    board.set_pin_mode_digital_input_pullup(inPB1) # Pushbutton -> Digital Pullup Resistor
    for idx in outTL4:
        board.set_pin_mode_digital_output(outTL4[idx]) # Traffic Light LEDs (#1-3) -> Digital Output
    
    for idx in outPL1:
        board.set_pin_mode_digital_output(outPL1[idx]) # Pedestrian Light LEDs (#1-2) -> Digital Output

def get_inputs() -> bool:
    """
    Checks all input pins (currently only a pushbutton) for their current value

    PARAMETERS:
    None

    RETURNS:
    pushButtonState
    """

    pbState = True if board.digital_read(inPB1)[0] == 0 else False

    return pbState

def pb_pressed():
    """
    Logic handler for whenever a pushbutton press is registered

    PARAMETERS:
    None

    RETURNS:
    None
    """
    print("PB1 Pressed")
    
    change_light(outTL4, "Y")
    time.sleep(2)

    change_light(outTL4, "R")

    change_light(outPL1, "G")
    time.sleep(3)

    flash_light(outPL1, "R", 200, 2)

    change_light(outPL1, "R")
    change_light(outTL4, "G")
    

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
            board.digital_write(lightSet[light], 1)
        else:
            board.digital_write(lightSet[light], 0)


def flash_light(lightSet: dict, lightPin: str, interval: int, length: int):
    """
    PARAMATERS:
    lightSet -> The set of output LEDs to be modified
    lightPin -> The LED within lightSet to be flashed on and off
    interval -> The amount of time in ms that the Arduino will wait between each change in state
    length -> The time in seconds that the function will run

    RETURNS:
    None
    """
    startTime = time.time()

    for light in lightSet: # Turns off all LEDs in light set
        board.digital_write(lightSet[light], 0)

    while time.time() - startTime <= length: # Checks to make sure the function hasn't been running longer than the given length
        board.digital_write(lightSet[lightPin], 1)
        time.sleep(interval / 1000)
        board.digital_write(lightSet[lightPin], 0)
        time.sleep(interval / 1000)

if __name__ == "__main__":
    # Initialise UNO
    board = pymata4.Pymata4()
    setup()
    time.sleep(0.1)
    main()