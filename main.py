from subsystems import tunnel_ave_subsytem as s2
from pymata4 import pymata4
import time

def setup():
    # Configure Input Pins

    # Configure Output Pins
    pass

def main():
    while True:
        try:
            pass
        except KeyboardInterrupt as e:
            print('Ending Program')
            board.shutdown()
            raise e

if __name__ == "__main__":
    board = pymata4.Pymata4()