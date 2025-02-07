#
#
# TEST the PWM output
#
from sys import stdin, exit
from _thread import start_new_thread
from utime import sleep


from machine import ADC, Timer, Pin, UART, PWM


#########################################################
# SETUP PINS

# Define PWM pins
pwm_pins = [machine.Pin(pin, machine.Pin.OUT) for pin in range(16)]

# Create PWM objects for each pin
pwm_objects = [machine.PWM(pin) for pin in pwm_pins]


for pin in range(16):
    pwm_objects[pin].freq(10000)

# Function to set PWM duty cycle for a specific pin
def set_pwm(pin, duty_cycle):
    pwm_objects[pin].duty_u16(duty_cycle)

while True:

    for i in range(16):
        set_pwm(i, 65000)
        sleep(0.2)
    print("all on")
    for i in range(16):
        set_pwm(i, 0)
        sleep(0.2)
    print("all off")
    
 