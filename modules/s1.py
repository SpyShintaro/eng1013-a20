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

def execute(inputs, trafficRegister, warningRegister):

    match state["phase"]:
        case 0:
            if inputs["US1"]:
                print(f"Detected vehicle above height 4m at time: {time.time()}")
                utils.change_light(trafficRegister["TL1"], "Y")

                state["phase"] = 1
                state["clock"] = utils.sleep(1)

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["flashing"] = utils.flash_light(warningRegister["WL"], "WL1", warningInterval)
            else:
                utils.change_light(trafficRegister["TL1"], "G")
                utils.change_light(trafficRegister["TL2"], "G")

        case 1:
            state["flashing"] = utils.flash_light(warningRegister["WL"], "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])

            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL1"], "R")
                utils.change_light(trafficRegister["TL2"], "Y")

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["phase"] = 2
                state["clock"] = utils.sleep(1)
        
        case 2:
            state["flashing"] = utils.flash_light(warningRegister["WL"], "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL2"], "R")

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["phase"] = 3
                state["clock"] = utils.sleep(29)
        
        case 3:
            state["flashing"] = utils.flash_light(warningRegister["WL"], "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            if time.time() >= state["clock"]:
                utils.change_light(trafficRegister["TL1"], "G")

                print(trafficRegister["TL1"])
                print(trafficRegister["TL2"])

                state["phase"] = 4
                state["clock"] = utils.sleep(1)
        
        case 4:
            if time.time() >= state["clock"]:
                if inputs["US1"]:
                    state["flashing"] = utils.flash_light(warningRegister["WL"], "WL1", warningInterval, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
                else:
                    utils.change_light(trafficRegister["TL2"], "G")

                    print(trafficRegister["TL1"])
                    print(trafficRegister["TL2"])

                    state["phase"] = 0