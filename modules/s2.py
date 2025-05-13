from modules import utils
import time

state = {
    "run": True,
    "phase": 0,
    "clock": 0
}

def execute(inputs, register):
    match state["phase"]:

        case 0:
            if time.time() >= state["clock"]:
                if inputs["PB1"]:
                    utils.change_light(register["TL4"], "Y")
                    state["phase"], state["clock"] = 1, utils.sleep(2) # This just saves space by assigning two variables at the same time (i.e. state["phase"] = 1)
                    
                    print(register["TL4"])

        case 1:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL4"], "R")
                state["phase"], state["clock"] = 2, utils.sleep(5)

                print(register["TL4"])
        
        case 2:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL4"], "G")
                state["phase"], state["clock"] = 0, utils.sleep(15)

                print(register["TL4"])