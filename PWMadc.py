from machine import Pin, PWM, ADC
pwm = PWM(Pin(14))
adc = ADC(Pin(26))
pwm.freq(1000)
while True:
    duty = adc.read_u16()
    pwm.duty_u16(duty)
    for duty in range(0, 65025, 1):
        pwm.duty_u16(duty)
    sleep(0.0001)

#go backward with a step of -1

    for duty in range(65025, 0.5, -1):
        pwm.duty_u16(duty)
        sleep(0.0005)
        
    sleep(2)