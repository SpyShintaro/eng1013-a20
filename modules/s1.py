import time
from modules import utils

warningInterval = 0.5

state = {
    "phase": 0,
    "clock": 0,
    "buzzer": {
        "activated": 0
    },

    "flashing": {
        "start": 0,
        "phase": 0,
        "clock": 0
    }
}

# if state["activated"] < int(duration*frequency):
#     board.digitalwrite()
#     sleep
#     board.board.set_pin_mode_digital_input
#     sleep
#     state["activated"] += 1

def execute(inputs: dict, trafficRegister: dict, warningRegister: dict) -> None:

    """
    Primary Function for S1, containing all required and general features

    PARAMETERS:
    inputs -> A dictionary containing all incoming input signals labelled with their component names
    trafficRegister -> A dictionary containing pin data to be sent to the TL3 shift register
    warningRegister -> A dictionary containing pin data to be sent to the WL1 shift register

    RETURNS:
    None
    """

    match state["phase"]:
        case 0:
            if inputs["US1"]:
                state["phase"], state["clock"] = 0.5, utils.sleep(0.5)
                print("started check")
            else:
                utils.change_light(trafficRegister["TL1"], "G")
                utils.change_light(trafficRegister["TL2"], "G")
        
        case 0.5: # Noise filtering
            if time.time() >= state["clock"]:
                if inputs["US1"]:
                    print("Vehicle Detected")
                    print(f"Detected vehicle above height 4m at time: {time.time()}")
                    utils.change_light(trafficRegister["TL1"], "Y")
                    utils.change_light(trafficRegister["TL2"], "G")

                    state["phase"] = 1
                    state["clock"] = utils.sleep(1)

                    print(trafficRegister["TL1"])
                    print(trafficRegister["TL2"])

                    state["flashing"] = utils.flash_light(warningRegister, "WL1", warningInterval)
                    utils.pin_on(warningRegister, "PA1") # Activates lower frequency piezo signal
                else:
                    utils.change_light(trafficRegister["TL1"], "G")
                    utils.change_light(trafficRegister["TL2"], "G")
                    state["phase"] = 0

        case 1:
            state["flashing"] = utils.flash_light(warningRegister, "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])

            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL1"], "R")
                utils.change_light(trafficRegister["TL2"], "Y")

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["phase"] = 2
                state["clock"] = utils.sleep(1)
        
        case 2:
            state["flashing"] = utils.flash_light(warningRegister, "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL2"], "R")

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["phase"] = 3
                state["clock"] = utils.sleep(29)
        
        case 3:
            state["flashing"] = utils.flash_light(warningRegister, "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            if time.time() >= state["clock"]:
                if inputs["US1"]:
                    state["flashing"] = utils.flash_light(warningRegister, "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
                    utils.pin_on(warningRegister, "PA1 High")
                else:
                    utils.change_light(trafficRegister["TL2"], "G")
                    utils.pin_off(warningRegister, "PA1")
                    utils.pin_off(warningRegister, "PA1 High")
                    utils.pin_off(warningRegister, "WL1")

                    print(trafficRegister["TL1"])
                    print(trafficRegister["TL2"])

                    state["phase"] = 0