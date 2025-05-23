from modules import utils
import time

state = {
    "US3": False,
    "phase": 0,
    "clock": 0,
    "start": 0,

    "flashing": {
        "start": 0,
        "phase": 0,
        "clock": 0,
    },

    "triggered": False # Checking if integration feature has been triggered
}

def execute(inputs: dict, trafficRegister: dict, lightsRegister: dict):
    """
    Primary loop function for subsystem 3

    PARAMETERS:
    inputs -> Dictionary containing all incoming inputs from Arduino pins
    trafficRegister -> Shift Register containing the subsystem's traffic lights
    lightsRegister -> Shift register containing the floodlights
    """

    match state["phase"]:
        case 0:
            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL5"], "R")
                if inputs["US3"]:
                    state["start"] = time.time()
                    state["phase"], state["clock"] = 0.5, utils.sleep(0.5)
                else:
                    utils.pin_off(lightsRegister, "FL")
                    state["US3"] = False
        
        case 0.5: # Noise filtering
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    utils.change_light(trafficRegister["TL5"], "Y")
                    state["phase"] = 1
                    state["clock"] = utils.sleep(2)

                    if inputs["DS1"]:
                        utils.pin_on(lightsRegister, "FL")
                    else:
                        utils.pin_off(lightsRegister, "FL")
                else:
                    state["phase"] = 0
                    state["US3"] = False
                    utils.pin_off(lightsRegister, "FL")
    
        case 1:
            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL5"], "G")
                state["phase"] = 2
                state["clock"] = utils.sleep(5)

                if inputs["DS1"]:
                    utils.pin_on(lightsRegister, "FL")
                else:
                    utils.pin_off(lightsRegister, "FL")
        
        case 2:
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    state["flashing"] = utils.flash_light(trafficRegister["TL5"], "G", 0.5)
                    state["phase"] = 3

                    if inputs["DS1"]:
                        utils.pin_on(lightsRegister, "FL")
                    else:
                        utils.pin_off(lightsRegister, "FL")
                    
                else:
                    utils.change_light(trafficRegister["TL5"], "R")
                    state["phase"] = 0
                    state["clock"] = 0
                    state["US3"] = False
        
        case 3:
            if inputs["US3"]:
                state["flashing"] = utils.flash_light(trafficRegister["TL5"], "G", 0.5, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])

                if inputs["DS1"]:
                    utils.pin_on(lightsRegister, "FL")
                else:
                    utils.pin_off(lightsRegister, "FL")
            else:
                state["phase"] = 0
                state["US3"] = False

def integration(inputs):
    if inputs["US3"]:
        state["triggered"] = True
    else:
        if state["triggered"] == True:
            state["triggered"] = False
            return 0