from machine import ADC, Pin
from time import sleep

photoPIN = 27
led = Pin(15, Pin.OUT)

def readLight(photoGP):
    photoRes = ADC(Pin(photoPIN))
    light = photoRes.read_u16()
    lightPerc = light*100/65535

    return lightPerc

while True:
    print("lightPerc:", readLight(photoPIN))
    sleep(0.01) # set a delay between readings
