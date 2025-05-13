from pymata4 import pymata4
import time

from modules import utils, s2

shiftReg1 = { # First Shift Register Handles TL1, TL2, and TL3 outputs

    "TL1": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "TL2": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "TL3": {
        "R": 0,
        "G": 0
    },

}
shiftReg2 = { # TL4, TL5, PL1
    "TL4": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "TL5": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "PL1": {
        "R": 0,
        "G": 0
    },
}
shiftReg3 = { # Everything Else
    "PA1": 0,
    "WL1": 0,
    "WL2": 0,
    "FL": 0,
    "US1": 0,
    "US2": 0,
    "US3": 0
}

run = {
    "s1": True,
    "s2": True,
    "s3": True,
    "s4": True
}

def setup():
    # Configure Input Pins

    # Configure Output Pins
    
    # Initialize main loop
    time.sleep(0.001)
    main()

def main():
    
    while True:
        try:

            # Get Inputs
            inputs = utils.get_inputs() # <- Testing for pushbutton being pressed

            # Handle Integration Features First

            # Code to decide


            # Requirements and General Features
            if run["s1"]:
                pass # Call subsystem 1 code

            if run["s2"]:
                s2.execute(inputs, shiftReg2) # Executes subsystem 2
            
            if run["s3"]:
                pass # Call subsytem 3

            if run["s4"]:
                pass # Call subsystem 4
        
        except KeyboardInterrupt as e:
            print('Ending Program')
            #board.shutdown()
            raise e

if __name__ == "__main__":
    #board = pymata4.Pymata4()
    setup()