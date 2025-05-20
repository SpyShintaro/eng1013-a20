#M2 Subsystem 4: Tunnel Height Detection Subsystem.
#Created By: Jessica Hu
#Created Date: 14 May 2025
#Version: 2.0
import time
from modules import utils

state = {
    "phase": 0,
    "clock": 0,

    "flashing-1": { # Controls the first warning LED
        "start": 0,
        "phase": 0,
        "clock": 0,
    },

    "flashing-2": { # Controls the second warning LED
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
                utils.kill_lights(warning_register["WL"])
        
        case 1: # Overheight vehicle detected: start flashing first warning light
            state["flashing-1"] = utils.flash_light(warning_register["WL"], "WL1", warning_interval)
            state["phase"], state["clock"] = 2, utils.sleep(warning_interval)
        
        case 2: # Overheight vehicle still detected: start flashing second warning light 0.5 seconds after first warning light
            if inputs["US2"]:
                if time.time() >= state["clock"]:
                    state["flashing-1"] = utils.flash_light(warning_register["WL"], "WL1", warning_interval, state["flashing-1"]["start"], state["flashing-1"]["phase"], state["flashing-1"]["clock"])
                    state["flashing-2"] = utils.flash_light(warning_register["WL"], "WL2", warning_interval)

                    state["phase"] = 3
                else:
                    state["flashing-1"] = utils.flash_light(warning_register["WL"], "WL1", warning_interval, state["flashing-1"]["start"], state["flashing-1"]["phase"], state["flashing-1"]["clock"])
            
            else:
                state["phase"] = 0
        
        case 3: # Overheight vehicle detected: continue flashing both lights simultaneously
            if inputs["US2"]:
                state["flashing-1"] = utils.flash_light(warning_register["WL"], "WL1", warning_interval, state["flashing-1"]["start"], state["flashing-1"]["phase"], state["flashing-1"]["clock"])
                state["flashing-2"] = utils.flash_light(warning_register["WL"], "WL2", warning_interval, state["flashing-2"]["start"], state["flashing-2"]["phase"], state["flashing-2"]["clock"])
            else:
                state["phase"] = 0

def integration(inputs, register, run):
    if inputs["US2"]:
        run["s2"] = False
        utils.change_light(register["TL4"], "R")