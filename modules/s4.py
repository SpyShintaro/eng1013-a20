<<<<<<< HEAD
#Created By: Jessica Hu
#Created Date: 14 May 2025
#Version: 2.0
from pymata4 import pymata4
from modules import utils
#import time
import math 
board = pymata4.Pymata4()

#set pin number
#US2
triggerPin = 9
echoPin = 8
#TL3
greenLightPin = 5
redLightPin = 4
#WL2(2 sets of 2, parallel resistor)
warningLightPin1 = 10
warningLightPin2 = 11

#configure pin mode as sonar
board.set_pin_mode_sonar(triggerPin, echoPin, timeout=10000000)
board.set_pin_mode_digital_output(greenLightPin)
board.set_pin_mode_digital_output(redLightPin)
board.set_pin_mode_digital_output(warningLightPin1)
board.set_pin_mode_digital_output(warningLightPin2)

def warning_light(a):
    """
    description: this function turns on the warning lights
    parameters: None
    returns: None
    """
    frequency = a
    timeBetweenFlash = 1/frequency  

    board.digital_write(warningLightPin1, 1)
    board.digital_write(warningLightPin2, 0)
    #time.sleep(timeBetweenFlash)
    utils.sleep(timeBetweenFlash)
    board.digital_write(warningLightPin1, 0)
    board.digital_write(warningLightPin2, 1) 
    #time.sleep(timeBetweenFlash)
    utils.sleep(timeBetweenFlash)       

def tunnel_height_detection_subsystem():
    """
    description: this function brings all components of subsystem 4 together, traffic light turns red once the sensor detects overheight traffic and turns green when no verheight traffic detected
    parameters: None
    returns: result[0]
    """

    print("CTRL+C to end program")

    try:
        board.digital_write(greenLightPin, 1)
        board.digital_write(redLightPin, 0)

        while True:
            result = board.sonar_read(triggerPin)
            recentReadings = []
            #noice filtering 
            while True:
                    
                if len(recentReadings) < 5:  
                    recentReadings.append(board.sonar_read(triggerPin))
                    #time.sleep(0.5)
                    utils.sleep(0.5)       

                elif len(recentReadings) > 5:  
                    recentReadings.pop(0)
                    #tolerance of 5cm
                    if recentReadings.max - recentReadings.min < 5:
                        break
                break

            if 2 <= result[0] <= 100:
                distance = result[0]
            
                board.digital_write(greenLightPin, 0)
                board.digital_write(redLightPin, 1)  
                #warning_light(5)            
            else:
                board.digital_write(greenLightPin, 1)
                board.digital_write(redLightPin, 0) 

    except KeyboardInterrupt:
        board.digital_write(greenLightPin, 0)
        board.digital_write(redLightPin, 0) 
        board.shutdown()
    return result[0]  

    

#main
tunnel_height_detection_subsystem()


=======
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

def execute(inputs, traffic_register, warning_register):
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
>>>>>>> 26fdfb4fc75b17d894cac98f4474341b736fdfac
