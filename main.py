from subsystems import tunnel_ave_subsytem as s2
from pymata4 import pymata4
import time

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

shiftReg2 = {
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

shiftReg3 = {
    "PA1": 0,
    "WL1": 0,
    "WL2": 0,
    "FL": 0,
    "US1": 0,
    "US2": 0,
    "US3": 0
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
            # Run Base Functions (most integration functions overwrite base functionality)?
            runS1 = True
            runS2 = True
            runS3 = True
            runS4 = True
            runs5 = True

            # Handle Integration Features First


            # Requirements and General Features
            pass
        
        except KeyboardInterrupt as e:
            print('Ending Program')
            board.shutdown()
            raise e
    
def get_inputs() -> dict:
    # Reads all inputs from the R-2R Ladder
    return {
        "PB1": False,
        "US1": False,
        "US2": False,
        "US3": False
    }

def sleep(duration: float) -> float:
    """
    Function for assigning soft delay in between processes

    PARAMETERS:
    duration: Time in seconds of delay

    RETURN:
    endTime: The time at which the process should resume
    """
    return time.time() + duration


def handle_outputs():
    pass

if __name__ == "__main__":
    board = pymata4.Pymata4()