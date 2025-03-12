from machine import Pin
import utime

pins = [Pin(15,Pin.OUT),Pin(14,Pin.OUT),Pin(16,Pin.OUT),Pin(17,Pin.OUT)]

full_step_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
full_step_sequence_rev = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]


def go_forward(num_step):
    for j in range(num_step):
        for step in full_step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)
def go_back(num_step):
    for j in range(num_step):
        for step in full_step_sequence_rev:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)

while True:
    go_forward(100)
    go_back(100)

    