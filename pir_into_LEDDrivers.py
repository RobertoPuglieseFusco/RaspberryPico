from machine import Pin, PWM
from time import sleep

pir = Pin(6, Pin.IN)

pwm = PWM(Pin(19))
led1 = PWM(Pin(2))
led2 = PWM(Pin(3))

pwm.freq(1000)
led1.freq(1000)
led2.freq(1000)
pwm.duty_u16(0)
led1.duty_u16(0)
led2.duty_u16(0)

while True:
    
    logic_state = pir.value()
    print ("the logic state value is:", logic_state)
    sleep(0.1)
    if logic_state == True:     # if push_button pressed
       
        #print("Pressed")
        for duty in range(0, 65025, 1):
            pwm.duty_u16(duty)
            led1.duty_u16(duty)
            led2.duty_u16(duty)
            sleep(0.0001)        
        sleep(0.2)
        for duty in range(65025, 0.5, -1):
            pwm.duty_u16(duty)
            led1.duty_u16(duty)
            led2.duty_u16(duty)
            sleep(0.0005)    
