#M2 Subsystem 4: Tunnel Height Detection Subsystem.
#Created By: Jessica Hu & Abbey Hubbard
#Created Date: 15 April 2025
#Version: 1.0
from pymata4 import pymata4
import time
board = pymata4.Pymata4()

def tunnel_height_detection_subsystem():
    """
    description: this function brings all components of subsystem 4 together, traffic light turns red once the sensor detects overheight traffic and turns green when no verheight traffic detected
    parameters: None
    returns: result[0]
    """
    
    #set pin number
    #US2
    triggerPin = 8
    echoPin = 9
    #TL3
    greenLightPin = 5
    redLightPin = 4
    #WL2(2 sets of 2, parallel resistor)
    warningLightPin = 3

    #configure pin mode as sonar
    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=10000000)
    board.set_pin_mode_digital_output(greenLightPin)
    board.set_pin_mode_digital_output(redLightPin)
    board.set_pin_mode_digital_input(warningLightPin)

    print("CTRL+C to end program")

    try:
        board.digital_write(greenLightPin, 1)
        board.digital_write(redLightPin, 0)
        while True:
            time.sleep(0.5)
            result = board.sonar_read(triggerPin)

            result = board.sonar_read(triggerPin)

            if 2 <= result[0] <= 100:
                distance = result[0]
                print(f"Distance from sensor: {distance} cm")
                print("Overheight vehicle detected")
              
                board.digital_write(greenLightPin, 0)
                board.digital_write(redLightPin, 1)              
            else:
                print("No object detected")
                board.digital_write(greenLightPin, 1)
                board.digital_write(redLightPin, 0) 
    except KeyboardInterrupt:
        board.digital_write(greenLightPin, 0)
        board.digital_write(redLightPin, 0) 
        board.shutdown()
    return result[0]  

    #while redLightPin.value()        

#main
#tunnel_height_detection_subsystem()
redLightPin = 4
greenLightPin = 5
board.set_pin_mode_digital_output(greenLightPin)
board.set_pin_mode_digital_output(redLightPin)
board.digital_write(redLightPin, 1)
time.sleep(3)
board.digital_write(redLightPin, 0)
if redLightPin==0:
    board.digital_write(greenLightPin, 1)
time.sleep(3)
board.digital_write(redLightPin, 1)
board.shutdown()


