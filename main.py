from pymata4 import pymata4
import time

from modules import utils, s1, s2, s3, s4

debug = False

pinSet = {
    "inputs": {},

    "outputs": {
        "SRCLK": 3,
        "RCLK": 4,
        "SER1": 5,
        "SER2": 6,
        "SER3": 7
    }
}

shiftReg1 = { # First Shift Register Handles TL1, TL2, and TL3 outputs

    "TL1": {
        "R": 0,
        "Y": 0,
        "G": 1
    },

    "TL2": {
        "R": 0,
        "Y": 0,
        "G": 1
    },

    "TL3": {
        "R": 0,
        "G": 1
    },

}
shiftReg2 = { # TL4, TL5, PL1
    "TL4": {
        "R": 0,
        "Y": 0,
        "G": 1
    },

    "TL5": {
        "R": 1,
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
    "FL": 1,
    "US1": 0,
    "US2": 0,
    "US3": 1,
    "None": 0
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
    
    while True:
        try:

            run["s1"] = True
            run["s2"] = True
            run["s3"] = True
            run["s4"] = True


            # print(f"Previous: {currentReg3['WL']}")

            # Get Inputs
            if not debug: # When Arduinois connected, we need to tell the function we're not debugging, and give it our board variable
                inputs = utils.get_inputs(False, board)
            else:
                inputs = utils.get_inputs(True)

            # Handle Integration Features First
            s4.integration(inputs, shiftReg2, run)

            # Requirements and General Features
            if run["s1"]:
                s1.execute(inputs, shiftReg1, shiftReg3)

            if run["s2"]:
                s2.execute(inputs, shiftReg2) # Executes subsystem 2
            
            if run["s3"]:
                s3.execute(inputs, shiftReg2, shiftReg3)

            if run["s4"]:
                s4.execute(inputs, shiftReg1, shiftReg3, run)
            
            if run["s2"]:
                s2.execute(inputs, shiftReg2) # Executes subsystem 2
            
            if not debug:
                utils.handle_outputs(board, shiftReg1, shiftReg2, shiftReg3, pinSet)
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

    inputs = pinSet["inputs"]
    outputs = pinSet["outputs"]
    for pin in outputs:
        board.set_pin_mode_digital_output(outputs[pin])

    for pin in inputs:
        board.set_pin_mode_digital_input(inputs[pin])

    board.set_pin_mode_analog_input(0) # This will be the pin connected to PB1

    board.set_pin_mode_sonar(9, 8, timeout=10000000)
    board.set_pin_mode_sonar(11, 10, timeout=10000000)
    board.set_pin_mode_sonar(13, 12, timeout=10000000)

    time.sleep(0.1)

    main()


if __name__ == "__main__":
    if not debug:
        board = pymata4.Pymata4()
        setup()
    else:
        debug_setup()