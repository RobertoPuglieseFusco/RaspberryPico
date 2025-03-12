from machine import Pin
from time import sleep


push_button = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    logic_state = push_button.value()
    print ("the logic state value is:", logic_state)
    sleep(0.1)
    