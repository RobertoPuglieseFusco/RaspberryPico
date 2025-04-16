from machine import Pin
from time import sleep

reed = Pin(16,Pin.IN,Pin.PULL_UP)
led = machine.Pin("LED", machine.Pin.OUT)

def btn_handler(pin):
    if reed.value()==0:
        print("Magnet")        
        led.on()
    else:
        print("No magnet")
        led.off()
    
#reed.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING,handler=btn_handler)

prevValue = 1

while True:
    
    count = 0
    timeInit = 0
    prevValue = 0
    
    while timeInit < 1:
        
        if reed.value()==0 and prevValue == 1:
            #print("Magnet")        
            led.on()
            count = count + 1
            prevValue = 0
        else:
            #print("No magnet")
            led.off()
            prevValue = 1
        sleep(0.01)
        timeInit = timeInit + 0.01
        
    bpm = count
    
    print(bpm)
    