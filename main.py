from pymata4 import pymata4
import time

from modules import utils, s2, s3, s4

from modules import utils, s2
debug = True # False when the Arduino is connected

shiftReg1 = { # First Shift Register Handles TL1, TL2, and TL3 outputs

    "TL1": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "TL2": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "TL3": {
        "R": 0,
        "G": 0
    },

}
shiftReg2 = { # TL4, TL5, PL1
    "TL4": {
        "R": 0,
        "Y": 0,
        "G": 1
    },

    "TL5": {
        "R": 0,
        "Y": 0,
        "G": 0
    },

    "PL1": {
        "R": 1,
        "G": 0
    },
}
shiftReg3 = { # Everything Else
    "PA1": 0,
    "WL":{
        "WL1": 0,
        "WL2": 0,
    },
    "FL": 0,
    "US1": 0,
    "US2": 0,
    "US3": 0
}

run = {
    "s1": True,
    "s2": True,
    "s3": True,
    "s4": True
}

def debug_setup():
    # Configure Input Pins

    # Configure Output Pins
    
    # Initialize main loop
    time.sleep(0.001)
    main() 

def main():

    oldReg1, oldReg2, oldReg3 = shiftReg1, shiftReg2, shiftReg3 # Comparison
    
    while True:
        try:

            # print(f"Previous: {currentReg3['WL']}")

            # Get Inputs
            if not debug: # When Arduinois connected, we need to tell the function we're not debugging, and give it our board variable
                inputs = utils.get_inputs(False, board)
            else:
                inputs = utils.get_inputs(True)

            # Handle Integration Features First

            # Code to decide


            # Requirements and General Features
            if run["s1"]:
                s1.execute(inputs, [shiftReg1, shiftReg3]) #Executes subsystem 1 code

            if run["s2"]:
                s2.execute(inputs, shiftReg2) # Executes subsystem 2
            
            if run["s3"]:
                s3.execute(inputs, shiftReg2)

            if run["s4"]:
                s4.execute(inputs, shiftReg1, shiftReg3)
            
            if not debug:
                utils.handle_outputs(board, shiftReg1, shiftReg2, shiftReg3)
                time.sleep(0.001) # Leave this in or the Arduino freaks tf out
        
            # print(f"Current: {shiftReg3['WL']}")
        
        except KeyboardInterrupt as e:
            print('Ending Program')
            board.shutdown()
            raise e

def setup():
    """
    Gonna be the main setup function once everything is implemented, but for now I'm just using it for testing
    """
    
    board.set_pin_mode_digital_output(6) # TL4 Red
    board.set_pin_mode_digital_output(5) # TL4 Yellow
    board.set_pin_mode_digital_output(4) # TL4 Green
    
    board.set_pin_mode_digital_output(10) # WL1
    board.set_pin_mode_digital_output(11) # WL2

    board.set_pin_mode_digital_input_pullup(12)
    board.set_pin_mode_sonar(9, 8, timeout=10000000)

    main()


if __name__ == "__main__":
    if not debug:
        board = pymata4.Pymata4()
        setup()
    else:
        debug_setup()