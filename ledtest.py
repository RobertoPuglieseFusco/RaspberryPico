from machine import Pin
from time import sleep
push_button = Pin(0, Pin.IN, Pin.PULL_UP)

led = Pin(19, Pin.OUT)    # 14 number in is Output


while True:  
    logic_state = push_button.value()
    #print ("the logic state value is:", logic_state)
    sleep(0.01)
    if logic_state == True:     # if push_button pressed
        led.value(1)             # led will turn ON
        #print("Pressed")
        sleep(0.2)
    else:                       # if push_button not pressed
        led.value(0)             # led will turn OFF