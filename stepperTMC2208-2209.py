## using TMC2208/2209

## https://a.pololu-files.com/picture/0J4232.1200.png?f2f6269e0a80c41f0a5147915106aa55

# POWER:
# 12V → VMOT
# GND → GND
# Pico GND → TMC GND
# 
# CONTROL:
# Pico GP14 → TMC STEP
# Pico GP15 → TMC DIR
# Pico GP13 → TMC EN (enable)
# 
# MICROSTEPPING (hardware pins):
# MS1 → GND or 3.3V
# MS2 → GND or 3.3V
# (See table below)
# 
# MOTOR:
# Motor coils → B2, B1, A1, A2

# MS1   MS2  | Resolution
# ------------|------------------
# GND   GND  | 1/8 step (default)
# 3V3   GND  | 1/2 step
# GND   3V3  | 1/4 step
# 3V3   3V3  | 1/16 step

from machine import Pin
from time import sleep, sleep_us

step = Pin(14, Pin.OUT)
dir_pin = Pin(15, Pin.OUT)
enable_pin = Pin(13, Pin.OUT)

MICROSTEPS = 16  # Change from 32 to 16
STEPS_PER_REV = 200 * MICROSTEPS  # Now 3200
STEPS_PER_DEGREE = STEPS_PER_REV / 360

def motor_on():
    enable_pin.value(0)
    sleep(0.01)

def motor_off():
    enable_pin.value(1)

def move_degrees(degrees, speed_us=500):
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
move_degrees(90, 5000)  # Higher = slower, smoother
sleep(2)

print("180° counterclockwise...")
move_degrees(-180, 10000)
sleep(2)

print("90° back to center...")
move_degrees(90, 100)

print("Complete!")