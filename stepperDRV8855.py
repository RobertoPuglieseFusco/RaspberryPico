## using DRV8855

from machine import Pin
from time import sleep, sleep_us

step = Pin(14, Pin.OUT)
dir_pin = Pin(15, Pin.OUT)
enable_pin = Pin(13, Pin.OUT)

MICROSTEPS = 32  # Keep 1/32 for smoothness
STEPS_PER_DEGREE = (200 * MICROSTEPS) / 360

def motor_on():
    enable_pin.value(0)
    sleep(0.01)

def motor_off():
    enable_pin.value(1)

def move_degrees(degrees, speed_us=2500):
    """Simple slow smooth movement"""
    steps = int(abs(degrees) * STEPS_PER_DEGREE)
    dir_pin.value(1 if degrees > 0 else 0)
    
    motor_on()
    
    for _ in range(steps):
        step.value(1)
        sleep_us(speed_us)
        step.value(0)
        sleep_us(speed_us)
    
    motor_off()
    print(f"Moved {degrees}°")

print("Slow smooth camera sequence")
sleep(2)

print("90° clockwise - very slow...")
move_degrees(90, 1000)  # Higher = slower, smoother
sleep(2)

print("180° counterclockwise...")
move_degrees(-180, 10000)
sleep(2)

print("90° back to center...")
move_degrees(90, 10000)

print("Complete!")