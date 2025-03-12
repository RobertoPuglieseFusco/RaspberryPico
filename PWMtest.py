from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(27))

pwm.freq(1000)

while True:
    for duty in range(0, 65025, 1):
        pwm.duty_u16(duty)
        sleep(0.0001)

#go backward with a step of -1

    for duty in range(65025, 0.5, -1):
        pwm.duty_u16(duty)
        sleep(0.0005)
        
    sleep(2)