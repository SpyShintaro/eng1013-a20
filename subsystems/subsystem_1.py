#By: Jess and Mirela
#Last edited date: 15th of April
#version number: 4

#M2 Subsystem 1: Approach Height Detection Subsystem. 
from pymata4 import pymata4
import time

board = pymata4.Pymata4()

#global variables:
#TL1
greenLightPin1 = 7
yellowLightPin1 = 6
redLightPin1 = 5

board.set_pin_mode_digital_output(greenLightPin1)
board.set_pin_mode_digital_output(yellowLightPin1)
board.set_pin_mode_digital_output(redLightPin1)

#TL2
greenLightPin2 = 4
yellowLightPin2 = 3
redLightPin2 = 2
    
board.set_pin_mode_digital_output(greenLightPin2)
board.set_pin_mode_digital_output(yellowLightPin2)
board.set_pin_mode_digital_output(redLightPin2)

#set pin number for the ultrasonic sensor
triggerPin = 8
echoPin = 9

board.set_pin_mode_sonar(triggerPin, echoPin, timeout=10000000)

#configure pin mode as sonar

#warning lights
warningLightPin1 = 12
warningLightPin2 = 13

board.set_pin_mode_digital_output(warningLightPin1)
board.set_pin_mode_digital_output(warningLightPin2)

#buzzer
buzzerPin = 11

board.set_pin_mode_digital_output(buzzerPin)

def approach_height_detection_subsystem():
    """
    description: this function brings together all components of subsystem 1.
    It starts off with both traffic lights as green and then calls both other functions of this subsystem in order to change it as needed.
    parameters: None
    returns: None
    """
    
    board.digital_write(greenLightPin1, 1)
    board.digital_write(yellowLightPin1, 0)
    board.digital_write(redLightPin1, 0)

    board.digital_write(greenLightPin2, 1)
    board.digital_write(yellowLightPin2, 0)
    board.digital_write(redLightPin2, 0)

    board.digital_pin_write(warningLightPin1, 0)
    board.digital_pin_write(warningLightPin2,0)

    board.digital_pin_write(buzzerPin,0)   

    timeOfDetection =  ulstrasonic_sensor1_dependent()
    
    if timeOfDetection > 0:
        traffic_light_system1()

def ulstrasonic_sensor1_dependent():
    """
    description: this function defines how the ultrasonic sensor works and records data
    parameters: None
    returns: result[1] - the time of detection of an overheight vehicle
    """
    #universal variables
    result=[]
    while True:

        endtime = sleep(0.2)
        while True:
            if time.time() >= endtime:
                break

        result=board.sonar_read(triggerPin)#read from the US1

        if (2<result[0]<100): #defined width of the road
            print("Vehicle height: 4m. Time of detection: ", result[1])
            timeOfDetection = result[1]
            return timeOfDetection
    
def traffic_light_system1():
    """
    description: this function starts the traffic light sequence for two traffic lights
    parameters: None
    returns: None
    """

    board.digital_pin_write(greenLightPin1,0)
    board.digital_pin_write(yellowLightPin1,1)
    #warning_lights_system1(5,1) 
    buzzer_system1(5,5)
    board.digital_pin_write(greenLightPin2,0)
    board.digital_pin_write(yellowLightPin2, 1)
    board.digital_pin_write(yellowLightPin1, 0)
    board.digital_pin_write(redLightPin1,1)
    #warning_lights_system1(5,1)
    buzzer_system1(5,5)
    board.digital_pin_write(yellowLightPin2,0)
    board.digital_pin_write(redLightPin2,1)
    #warning_lights_system1(5,5)
    buzzer_system1(5,5)

    while True:
        result = board.sonar_read(triggerPin)
        if result[0]<=2 or result[0]>=100: #defined width of the road
            break
        else:
            board.digital_pin_write(redLightPin1,1)
            board.digital_pin_write(redLightPin2,1)
            #warning_lights_system1(5,0.5)
            buzzer_system1(2005,0.5)
    

    board.digital_pin_write(redLightPin1, 0)
    board.digital_pin_write(greenLightPin1, 1)
    #warning_lights_system1(5,5)
    buzzer_system1(5,5)
    board.digital_pin_write(redLightPin2, 0)
    board.digital_pin_write(greenLightPin2, 1)

"""

def warning_lights_alert_buzzer_system1(a,b):
    frequency = a
    duration = b
    timeBetweenFlashes = 1/frequency
    for _ in range(int(duration*frequency)):
        board.digital_pin_write(warningLightPin1, 1)
        board.digital_pin_write(warningLightPin2, 0)
        board.digital_pin_write(buzzerPin,1)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
        board.digital_pin_write(warningLightPin2, 1)
        board.digital_pin_write(warningLightPin1, 0)
        board.digital_pin_write(buzzerPin,0)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
                
                while warninglights_system1(5,1){  
                buzzer_system1(5,1)}

"""
"""
def warning_lights_system1(a,b):
    frequency = a
    duration = b
    timeBetweenFlashes = 1/frequency
    for _ in range(int(duration*frequency)):
        board.digital_pin_write(warningLightPin1, 1)
        board.digital_pin_write(warningLightPin2, 0)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
        board.digital_pin_write(warningLightPin2, 1)
        board.digital_pin_write(warningLightPin1, 0)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
      
def warning_lights_alarm_system1(a,b):
    frequency = a
    duration = b
    timeBetweenFlashes = 1/frequency
    for _ in range(int(duration*frequency)):
        board.digital_pin_write(warningLightPin1, 1)
        board.digital_pin_write(warningLightPin2, 0)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
        board.digital_pin_write(warningLightPin2, 1)
        board.digital_pin_write(warningLightPin1, 0)
        endtime = sleep(timeBetweenFlashes/2)
        while True:
            if time.time() >= endtime:
                break
"""
def buzzer_system1(a,b):
    frequency = a
    duration = b
    timeBetweenBuzzes = 1/frequency
    endtime = sleep(timeBetweenBuzzes/2)
    for _ in range(int(duration*frequency)):
        if time.time() >= endtime:
            board.digital_pin_write(buzzerPin,1)
            endtime = sleep(timeBetweenBuzzes/2)
            board.digital_pin_write(buzzerPin,0)
            endtime = sleep(timeBetweenBuzzes/2)

def sleep(duration: float) -> float:
    """
    Function for assigning soft delay in between processes

    PARAMETERS:
    duration: Time in seconds of delay

    RETURN:
    endTime: The time at which the process should resume
    """
    return time.time() + duration

while True:
    try: 
        approach_height_detection_subsystem()
    except KeyboardInterrupt:
        board.digital_pin_write(redLightPin1,0)
        board.digital_pin_write(yellowLightPin1,0)
        board.digital_pin_write(greenLightPin1,0)
        board.digital_pin_write(redLightPin2,0)
        board.digital_pin_write(yellowLightPin2,0)
        board.digital_pin_write(greenLightPin2,0)
        board.digital_pin_write(warningLightPin1, 0)
        board.digital_pin_write(warningLightPin2, 0)
        board.digital_pin_write(buzzerPin,0)   
        print("Program ending")
        board.shutdown()
        exit()