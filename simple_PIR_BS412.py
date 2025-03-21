from machine import ADC, Pin
from time import sleep


#-
#     Connect pin #1 to ground
#     Connect pin #2 to ground (on time of 2 seconds)
#     Connect pin #3 to 3.3V
#     Check signal on pin #4

#_

pir = Pin(6, Pin.IN)
led = Pin(19, Pin.OUT)    # 14 number in is Output

while True:
    logic_state = pir.value()
    print ("the logic state value is:", logic_state)
    sleep(0.1)
    if logic_state == False:     # if push_button pressed
        led.value(1)             # led will turn ON
        #print("Pressed")
        sleep(0.2)
    else:                       # if push_button not pressed
        led.value(0)             # led will turn OFF
    