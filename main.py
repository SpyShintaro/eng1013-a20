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

s1 = {
            "run": True,
            "phase": 0,
            "clock": 0
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
            inputs = get_inputs() # <- Testing for pushbutton being pressed

            # Run Base Functions (most integration functions overwrite base functionality)?
            runS1 = True
            runS2 = True
            runS3 = True
            runS4 = True
            runs5 = True

            # Handle Integration Features First


            # Requirements and General Features
            if s1["run"]:
                match s1["phase"]:
                    case 0:
                        if time.time() >= s1["clock"]:
                            if inputs["PB1"]:
                                print("crossing")
                                change_light(shiftReg2["TL4"], "Y")
                                s1["phase"], s1["clock"] = 1, sleep(2) # This just saves space by assigning two variables at the same time (i.e. s1["phase"] = 1)
                    
                    case 1:
                        if time.time() >= s1["clock"]:
                            change_light(shiftReg2["TL4"], "R")
                            s1["phase"], s1["clock"] = 2, sleep(5)
                    
                    case 2:
                        if time.time() >= s1["clock"]:
                            change_light(shiftReg2["TL4"], "G")
                            s1["phase"], s1["clock"] = 0, sleep(15)

        
        except KeyboardInterrupt as e:
            print('Ending Program')
            #board.shutdown()
            raise e
    
def get_inputs() -> dict:
    # Reads all inputs from the R-2R Ladder
    return {
        "PB1": True,
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


def handle_outputs():
    pass

if __name__ == "__main__":
    #board = pymata4.Pymata4()
    setup()