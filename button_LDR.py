from machine import ADC, Pin
from time import sleep

push_button = Pin(13, Pin.IN)
ledBUTTON = Pin(14, Pin.OUT) 
photoPIN = 26
ledLDR = Pin(15, Pin.OUT)

def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    if light < 30:     
        ledLDR.value(1)            
        print("Pressed")
    else:                       
        ledLDR.value(0)           
        print("Not pressed")

    return light

while True:
    logic_state = push_button.value()
    print ("the logic state value is:", logic_state)
    sleep(0.1)
    if logic_state == True:     # if push_button pressed
        ledBUTTON.value(1)             # led will turn ON
        print("Pressed")
    else:                       # if push_button not pressed
        ledBUTTON.value(0)             # led will turn OFF
        print("Not pressed")
      
    print("light: " + str(readLight(photoPIN)) +"%")
    sleep(1) # set a delay between readings