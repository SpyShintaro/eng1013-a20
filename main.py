from pymata4 import pymata4
import time

from modules import utils, s1, s2, s3, s4

debug = False # Set to False when we connect to Arduino

pinSet = { # Determining our input and output pins
    "inputs": {
        "PB1": 0,
        "DS1": 1
    }, # Analog input pins

    "outputs": {
        "SRCLK": 3,
        "RCLK": 4,
        "SER1": 5,
        "SER2": 6,
        "SER3": 7
    }
}

# Pin data for output nodes connected to shift registers
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
    "PA1 LOW": 0,
    "PA1 HIGH": 0,
    "WL1": 0,
    "WL2": 0,
    "FL": 1,
    "WL1 POWER": 0,
    "None 2": 1,
    "None 3": 1
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

def main() -> None:
    """
    Main loop that iterates through each subsystem

    PARAMETERS:
    None

    RETURNS:
    None
    """
    
    while True:
        try:

            start = time.time()

            # Determines whether default behaviours are overriden
            run["s1"] = True
            run["s2"] = True
            run["s3"] = True
            run["s4"] = True

            # Get Inputs
            if not debug: # When Arduino is connected, we need to tell the function we're not debugging, and give it our board variable
                inputs = utils.get_inputs(False, board)
            else:
                inputs = utils.get_inputs(True)

            # Handle Integration Features First
            # integ1 = s1.integration(inputs, shiftReg2)
            integ3 = s3.integration(inputs)
            integ4 = s4.integration(inputs, shiftReg1, shiftReg2, shiftReg3, run)

            if integ3: # Resets subsystem 1 to default state after subsystem 3 integration feature
                s1.state["phase"] = integ3
            
            if integ4: # Resets subsystem 2 to default state after subsystem 4 integration feature
                s2.state["phase"] = integ4
                s1.state["phase"] = integ4

            # Requirements and General Features (Default behaviour)
            if run["s1"]:
                s1.execute(inputs, shiftReg1, shiftReg3)

            if run["s2"]:
                s2.execute(inputs, shiftReg2)
            
            if run["s3"]:
                s3.execute(inputs, shiftReg2, shiftReg3)

            if run["s4"]:
                s4.execute(inputs, shiftReg1, shiftReg3, run)
            
            if not debug:
                utils.handle_outputs(board, shiftReg1, shiftReg2, shiftReg3, pinSet) # Sends all register and pin data
                time.sleep(0.001) # Leave this in or the Arduino freaks tf out
        
            # print(f"Current: {shiftReg3['WL']}")
        
        except KeyboardInterrupt as e:
            print('Ending Program')
            board.shutdown()
            exit()

def setup() -> None:
    """
    Configures all pins on Arduino

    PARAMETERS:
    None

    RETURNS:
    None
    """

    inputs = pinSet["inputs"]
    outputs = pinSet["outputs"]
    for pin in outputs:
        board.set_pin_mode_digital_output(outputs[pin])

    board.set_pin_mode_analog_input(0) # PB1
    board.set_pin_mode_analog_input(1) # LDR

    board.set_pin_mode_sonar(9, 8, timeout=10000000)
    board.set_pin_mode_sonar(11, 10, timeout=10000000)
    board.set_pin_mode_sonar(13, 12, timeout=10000000)

    time.sleep(0.01)

    main()


if __name__ == "__main__":
    if not debug: # When Arduino is connected, we can set up Pymata4
        board = pymata4.Pymata4()
        setup()
    else: # Otherwise, run a code only version of the program
        debug_setup()