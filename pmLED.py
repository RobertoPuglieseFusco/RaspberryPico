from machine import Pin, PWM, ADC
from time import sleep

pwm = PWM(Pin(12))

adc = ADC(Pin(27))

pwm.freq(1000)

while True:
    duty = adc.read_u16()
    print(duty)
    pwm.duty_u16(duty)
    sleep(0.2)

