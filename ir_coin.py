from machine import ADC, Pin
from time import sleep

photoPIN = 26
led = Pin(15, Pin.OUT)
ledGreen = Pin(13, Pin.OUT)
ledBlue = Pin(14, Pin.OUT)

def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    led.value(1)  
    if light < 49:
        ledGreen.value(1)
        print("Trigger")

    else:
        ledGreen.value(0)
        print("No trigger")

    return light

while True:
    print("light: " + str(readLight(photoPIN)) +"%")
    sleep(1) # set a delay between readings
