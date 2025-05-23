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
    },

    "integration": {
        "phase": 0,
        "flashing": {
            "start": 0,
            "phase": 0,
            "clock": 0
        }
    },

    "triggered": False
}

warningInterval = 0.5

def execute(inputs, traffic_register, warning_register, run):
    match state["phase"]:
        case 0: # No overheight vehicle detected
            if inputs["US2"]:
                state["clock"], state["phase"] = utils.sleep(0.5), 0.5
            else:
                utils.change_light(traffic_register["TL3"], "G")
                utils.pin_off(warning_register, "WL2")
        
        case 0.5:
            if state["clock"] <= time.time():
                if inputs["US2"]:
                    utils.change_light(traffic_register["TL3"], "R")
                    utils.pin_on(warning_register, "WL2")
                    state["phase"], state["clock"] = 1, utils.sleep(warningInterval)
                else:
                    state["phase"] = 0
        
        case 1: # Overheight vehicle detected: start flashing first warning light
            # state["flashing"] = utils.flash_light(warning_register, "WL2", warning_interval)
            state["phase"], state["clock"] = 2, utils.sleep(warningInterval)
        
        case 2: # Overheight vehicle detected: continue flashing both lights simultaneously
            if inputs["US2"]:
                pass
                # state["flashing"] = utils.flash_light(warning_register, "WL2", warning_interval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            else:
                utils.pin_off(warning_register, "WL2")
                state["phase"] = 0

def integration(inputs, register1, register2, register3, run):
    if inputs["US2"]:
        run["s2"], run["s1"] = False, False
        utils.change_light(register2["TL4"], "R")
        utils.change_light(register1["TL1"], "R")
        utils.change_light(register1["TL2"], "R")
        utils.pin_off(register3, "PA1 HIGH")
        utils.pin_on(register3, "PA1 LOW")
        utils.pin_on(register3, "WL1 POWER")
        state["triggered"] = True

        match state["integration"]["phase"]:
            case 0:
                state["integration"]["flashing"] = utils.flash_light(register3, "WL1", warningInterval)
                state["integration"]["phase"] = 1
            
            case 1:
                state["integration"]["flashing"] = utils.flash_light(register3, "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
    else:
        if state["triggered"]:
            state["triggered"] = False
            state["integration"]["phase"] = 0
            utils.change_light(register1["TL1"], "G")
            utils.change_light(register1["TL2"], "G")
            utils.pin_off(register3, "WL1 POWER")
            utils.pin_off(register3, "PA1 LOW")
            return 0