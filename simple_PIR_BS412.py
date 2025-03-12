from machine import ADC, Pin
from time import sleep

push_button = Pin(4, Pin.IN)

while True:
    logic_state = push_button.value()
    print ("the logic state value is:", logic_state)
    sleep(0.1)
    