from machine import Pin
import utime

# Define stepper motor control pins
pins = [Pin(15, Pin.OUT), Pin(14, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]

# Full-step sequence (Clockwise)
full_step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Reverse full-step sequence (Counterclockwise)
full_step_sequence_rev = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]

# Function to move stepper motor forward
def go_forward(num_step, delay=2):
    for _ in range(num_step):
        for step in full_step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
            utime.sleep_ms(delay)  # Small delay for motor movement

# Function to move stepper motor backward
def go_back(num_step, delay=2):
    for _ in range(num_step):
        for step in full_step_sequence_rev:
            for i in range(len(pins)):
                pins[i].value(step[i])
            utime.sleep_ms(delay)  # Small delay for motor movement

# Loop to move motor forward and backward
while True:
    go_forward(1000, delay=2)  # Adjust delay for speed control
    utime.sleep(1)  # Pause before reversing
    go_back(1000, delay=2)
    utime.sleep(1)  # Pause before repeating