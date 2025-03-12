from machine import Pin
from time import sleep

led = Pin(14, Pin.OUT)    # 14 number in is Output
push_button = Pin(13, Pin.IN)  # 13 number pin is input

while True:  
    logic_state = push_button.value()
    print ("the logic state value is:", logic_state)
    sleep(0.2)
    if logic_state == True:     # if push_button pressed
        led.value(1)             # led will turn ON
        print("Pressed")
    else:                       # if push_button not pressed
        led.value(0)             # led will turn OFF
        print("Not pressed")
