from pymata4 import pymata4
import time

#Initialise Board
board = pymata4.Pymata4()

board.set_pin_mode_analog_input(0)
time.sleep(0.1)

print(board.analog_read(0)[0])

board.shutdown()