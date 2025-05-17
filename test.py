""" from pymata4 import pymata4
import time

board = pymata4.Pymata4()

SRCLR_PIN = 2 # Shift Register Clear
SRCLK_PIN = 3 # Shift Register Clock
SER1_PIN = 4 # Serial Input Pin
RCLK_PIN = 5 # Copies the shift register values to the output register all at once

SER1 = {
    "A": 1,
    "B": 0,
    "C": 0,
    "D": 0,
    "E": 0,
    "F": 0,
    "G": 0,
    "H": 0
}

def setup():
    board.set_pin_mode_digital_output(SRCLR_PIN)
    board.set_pin_mode_digital_output(SRCLK_PIN)
    board.set_pin_mode_digital_output(SER1_PIN)
    time.sleep(0.1)
    board.digital_write(SRCLR_PIN, 1)

    shift_reg()

def update_shift():
    board.digital_write(SRCLR_PIN, 0)
    board.digital_write(SRCLR_PIN, 1)

    for pin in SER1:
        board.digital_write(SER1_PIN, SER1[pin])
        board.digital_write(SRCLK_PIN, 1)
        board.digital_write(SRCLK_PIN, 0)
    
    board.digital_write(RCLK_PIN, 1)
    board.digital_write(RCLK_PIN, 0)


def shift_reg():
    update_shift()

if __name__ == "__main__":
    setup() """

from pymata4 import pymata4
import time

# Pin configuration (adjust as needed)
DATA_PIN = 5     # SER (DS)
CLEAR_PIN = 2    # SRCLR (active LOW)
CLOCK_PIN = 3    # SRCLK (Shift clock)
LATCH_PIN = 4    # RCLK (Latch clock)

# Define bit order (Q0=A, Q1=B, ..., Q7=H)
BIT_ORDER = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Initialize board
board = pymata4.Pymata4()

# Set all control pins to OUTPUT
for pin in [DATA_PIN, CLEAR_PIN, CLOCK_PIN, LATCH_PIN]:
    board.set_pin_mode_digital_output(pin)

# === FAILSAFE CLEAR AT STARTUP ===
def clear_register():
    board.digital_write(CLEAR_PIN, 0)  # active LOW
    time.sleep(0.01)
    board.digital_write(CLEAR_PIN, 1)  # back to normal
    time.sleep(0.01)

# Simple pulse utility
def pulse(pin, delay=0.001):
    board.digital_write(pin, 1)
    time.sleep(delay)
    board.digital_write(pin, 0)
    time.sleep(delay)

# Main shift register write function
def write_shift_register(bit_dict):
    # Ensure correct bit order and padding
    bits = [bit_dict.get(k, 0) for k in BIT_ORDER]
    bits = list(reversed(bits))  # MSB first

    board.digital_write(LATCH_PIN, 0)      # Disable latch
    time.sleep(0.001)

    for bit in bits:
        board.digital_write(DATA_PIN, bit)
        pulse(CLOCK_PIN)

    board.digital_write(DATA_PIN, 0)       # Cleanup data line
    board.digital_write(LATCH_PIN, 1)      # Latch the output
    time.sleep(0.001)

# === MAIN LOOP ===
try:
    clear_register()  # Clear any residual state

    toggle = 0
    while True:
        # Update output dictionary
        SER = {
            "A": 1 - toggle,  # toggle A
            "B": toggle,      # toggle B
            "C": toggle,      # toggle C
            "D": 0,
            "E": 0,
            "F": 0,
            "G": 0,
            "H": 1 - toggle
        }
        write_shift_register(SER)

        toggle ^= 1
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrupted by user.")

finally:
    print("Clearing shift register and shutting down...")
    clear_register()
    board.shutdown()
