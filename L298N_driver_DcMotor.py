from machine import Pin, PWM
import time

# L298N connections to Pico
# Motor A
ENA = Pin(5, Pin.OUT)  # Enable pin for motor A
IN1 = Pin(7, Pin.OUT)  # Input 1
IN2 = Pin(8, Pin.OUT)  # Input 2

# PWM setup for speed control
pwm = PWM(ENA)
pwm.freq(1000)  # PWM frequency at 1kHz

def set_motor_speed(speed):
    """
    Set motor speed using PWM. Speed ranges from 0 (off) to 100 (full speed).
    """
    if speed < 0 or speed > 100:
        raise ValueError("Speed must be between 0 and 100")
    
    # Convert 0-100 to 0-65535 (16-bit PWM range)
    pwm_value = int(speed * 65535 / 100)
    pwm.duty_u16(pwm_value)

def motor_forward(speed=100):
    """
    Run motor forward at specified speed
    """
    IN1.value(1)
    IN2.value(0)
    set_motor_speed(speed)
    
def motor_backward(speed=100):
    """
    Run motor backward at specified speed
    """
    IN1.value(0)
    IN2.value(1)
    set_motor_speed(speed)
    
def motor_stop():
    """
    Stop the motor
    """
    IN1.value(0)
    IN2.value(0)
    set_motor_speed(0)

# Example usage
try:
    print("Motor forward at 50% speed")
    motor_forward(50)
    time.sleep(3)
    
    print("Motor backward at 75% speed")
    motor_backward(75)
    time.sleep(3)
    
    print("Motor forward at full speed")
    motor_forward(100)
    time.sleep(3)
    
except KeyboardInterrupt:
    # Stop motor on Ctrl+C
    motor_stop()
    print("Program stopped")