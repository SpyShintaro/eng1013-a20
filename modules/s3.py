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
    }
}

def execute(inputs, register):
    match state["phase"]:
        case 0:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL5"], "R")
                if inputs["US3"]:
                    print("started check")
                    state["start"] = time.time()
                    state["phase"], state["clock"] = 0.5, utils.sleep(0.5)
                else:
                    state["US3"] = False
        
        case 0.5: # Noise filtering
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    utils.change_light(register["TL5"], "Y")
                    state["phase"] = 1
                    state["clock"] = utils.sleep(2)
                    print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")

                    if inputs["DS1"]:
                        print("Turned Floodlights On")
                        utils.pin_on(register, "FL")
                    else:
                        print("Daylight")
                        utils.pin_off(register, "FL")
                else:
                    state["phase"] = 0
                    state["US3"] = False
                    utils.pin_off(register, "FL")
    
        case 1:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL5"], "G")
                state["phase"] = 2
                state["clock"] = utils.sleep(5)
                print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")
        
        case 2:
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    state["flashing"] = utils.flash_light(register["TL5"], "G", 0.5)
                    state["phase"] = 3
                    
                else:
                    utils.change_light(register["TL5"], "R")
                    state["phase"] = 0
                    state["clock"] = 0
                    state["US3"] = False
                    print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")
        
        case 3:
            if inputs["US3"]:
                state["flashing"] = utils.flash_light(register["TL5"], "G", 0.5, state["flashing"]["start"], state["flashing"]["phase"], state["flashing"]["clock"])
            else:
                state["phase"] = 0
                state["US3"] = False
                print("overheight vehicle no longer detected")