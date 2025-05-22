#M2 Subsystem 4: Tunnel Height Detection Subsystem.
#Created By: Jessica Hu
#Created Date: 14 May 2025
#Version: 2.0
from pymata4 import pymata4
from modules import utils
import time
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


