from modules import utils
import time

state = { # Stores information about the subsystem's current progress
    "phase": 0, # What stage of the program the subsytem is currently at
    "clock": 0,

    "flashing": {
        "start": 0,
        "phase": 0,
        "clock": 0,
    }
}

def execute(inputs, register):
    match state["phase"]:

        # Initial Phase
        case 0:
            if time.time() >= state["clock"]:
                if inputs["PB1"]:
                    print("crossing")
                    utils.change_light(register["TL4"], "Y")
                    state["phase"], state["clock"] = 1, utils.sleep(2) # This just saves space by assigning two variables at the same time (i.e. state["phase"] = 1)
                    
                    print(f"\033[0;92;49mTL4\033[0m: {register['TL4']}")

        case 1:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL4"], "R")
                utils.change_light(register["PL1"], "G")

                state["phase"], state["clock"] = 2, utils.sleep(3)

                print(f"\033[0;92;49mTL4\033[0m: {register['TL4']}")
                print(f"\033[0;92;49mPL1\033[0m: {register['PL1']}")
        
        case 2:
            if time.time() >= state["clock"]:
                state["phase"] = 3
                state["clock"] = utils.sleep(2)
                utils.change_light(register["PL1"], "R")

                state["flashing"] = utils.flash_light(register["PL1"], "R", 0.5)
                print(f"\033[0;92;49mTL4\033[0m: {register['TL4']}")
        
        case 3:
            if time.time() >= state["clock"]:
                state["phase"] = 4
            else:
                state["flashing"] = utils.flash_light(register["PL1"], "R", 0.5, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])

        case 4:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL4"], "G")
                
                utils.change_light(register["PL1"], "R")
                state["phase"], state["clock"] = 0, utils.sleep(15)

                print(f"\033[0;92;49mTL4\033[0m: {register['TL4']}")
