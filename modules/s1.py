#subsystem 1 integration attempt
import time
from pymata4 import pymata4
from utils import *
board = pymata4.Pymata4()

"""shiftReg1 = { # First Shift Register Handles TL1, TL2, and TL3 outputs

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

}"""

state = { # Stores information about the subsystem's current progress
    "phase": 0, # What stage of the program the subsytem
    "clock": 0
}

def execute(inputs, register):
    match state['phase']:
        case 0: #initial state of the function
            if time.time() >= state["clock"]:
                change_light(register["TL1"], "G")
                change_light(register["TL2"], "G")
                state["phase"], state["clock"] = 1, sleep() # This just saves space by assigning two variables at the same time (i.e. state["phase"] = 1)
                