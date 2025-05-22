from pymata4 import pymata4
import time

board = pymata4.Pymata4()

board.set_pin_mode_digital_output(8)

board.digital_write(8, 1)

board.shutdown()