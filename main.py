from subsystems import tunnel_ave_subsytem as s2
from pymata4 import pymata4
import time

"""
Resistor Ladder:

1 PB1
2. US1
"""

def setup():
    # Configure Input Pins

    # Configure Output Pins
    
    # Initialize main loop
    main()

def main():
    while True:
        try:
            # Run Base Functions (most integration functions overwrite base functionality)?
            runS1 = True
            runS2 = True
            runS3 = True
            runS4 = True
            runs5 = True

            # Handle Integration Features First

            # Requirements and General Features
            pass
        except KeyboardInterrupt as e:
            print('Ending Program')
            board.shutdown()
            raise e
    
def get_inputs() -> dict:
    # Reads all inputs from the R-2R Ladder
    return {
        "PB1": False,
        "US1": False,
        "US2": False,
        "US3": False
    }

if __name__ == "__main__":
    board = pymata4.Pymata4()