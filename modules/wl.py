from pymata4 import pymata4
import time

board = pymata4.Pymata4()

timer1 = 12
timer2 = 13

board.set_pin_mode_digital_output(timer1)
board.set_pin_mode_digital_output(timer2)


"""try:
        board.digital_write(13, 1)
        board.digital_write(12, 0)
        time.sleep(5)
        print("changing")
        board.digital_write(13, 0)
        board.digital_write(12, 1)
        time.sleep(5)
    except KeyboardInterrupt:
        print("ending")
        board.digital_write(timer1, 0)
        board.digital_write(timer2, 0)
        board.shutdown()"""
 
board.digital_write(12, 1)
time.sleep(4)
board.digital_write(12, 1)
board.shutdown()