#M2 Subsystem 4: Tunnel Height Detection Subsystem.
#Created By: Jessica Hu
#Created Date: 21 May 2025
#Version: 3.0
import time
from modules import utils

state = {
    "phase": 0,
    "clock": 0,

    "flashing": { # Controls the first warning LED
        "start": 0,
        "phase": 0,
        "clock": 0,
    }
}

warning_interval = 0.5

def execute(inputs, traffic_register, warning_register, run):
    match state["phase"]:
        case 0: # No overheight vehicle detected
            if inputs["US2"]:
                utils.change_light(traffic_register["TL3"], "R")
                state["phase"], state["clock"] = 1, utils.sleep(warning_interval)
            
            else:
                utils.change_light(traffic_register["TL3"], "G")
                utils.pin_off(warning_register, "WL2")
        
        case 1: # Overheight vehicle detected: start flashing first warning light
            state["flashing"] = utils.flash_light(warning_register, "WL2", warning_interval)
            state["phase"], state["clock"] = 2, utils.sleep(warning_interval)
        
        case 2: # Overheight vehicle detected: continue flashing both lights simultaneously
            if inputs["US2"]:
                state["flashing"] = utils.flash_light(warning_register, "WL2", warning_interval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            else:
                state["phase"] = 0

def integration(inputs, register, run):
    if inputs["US2"]:
        run["s2"] = False
        utils.change_light(register["TL4"], "R")
