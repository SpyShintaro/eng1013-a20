from modules import utils
import time

state = {
    "phase": 0,
    "clock": 0,
    "previous check": 0,
    "timer": 0
}

check_passed = True
next_check = utils.sleep(0.1)
us = True

if time.time() >= next_check:
    if us:
        vehicleDetected = True

def execute(inputs, register):
    match state["phase"]:
        case 0:
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    print("detected")
                    utils.change_light(register["TL5"], "Y")
                    state["phase"] = 1
                    state["clock"] = utils.sleep(2)
                    print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")
    
        case 1:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL5"], "G")
                state["phase"] = 2
                state["clock"] = utils.sleep(5)
                print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")
        
        case 2:
            if time.time() >= state["clock"]:
                utils.change_light(register["TL5"], "R")
                state["phase"] = 0
                state["clock"] = 0
                print(f"\033[0;91;49mTL5\033[0m: {register['TL5']}")
        
        case 3:
            if time.time() >= state["clock"]:
                if inputs["US3"]:
                    startTime = time.time()
                    state["phase"] = 4
                    
        case 4:
            if time.time() >= state["clock"]:
                pass