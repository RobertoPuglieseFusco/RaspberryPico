from machine import Pin, PWM
import time

class L9110S:
    def __init__(self, a1a_pin, a1b_pin, frequency=1000):
        """
        Initialize L9110S motor driver
        a1a_pin: Pin number for A1A (speed control)
        a1b_pin: Pin number for A1B (direction control)
        frequency: PWM frequency in Hz
        """
        self.motor_a = PWM(Pin(a1a_pin))
        self.motor_b = PWM(Pin(a1b_pin))
        
        # Set PWM frequency
        self.motor_a.freq(frequency)
        self.motor_b.freq(frequency)
        
        # Max duty cycle value (65535 for 16-bit PWM)
        self.max_duty = 65535
        
        # Stop motor initially
        self.stop()
    
    def forward(self, speed=100):
        """
        Run motor forward
        speed: 0-100 percentage
        """
        speed = min(100, max(0, speed))  # Clamp speed between 0-100
        duty = int(speed * self.max_duty / 100)
        self.motor_a.duty_u16(duty)
        self.motor_b.duty_u16(0)
    
    def backward(self, speed=100):
        """
        Run motor backward
        speed: 0-100 percentage
        """
        speed = min(100, max(0, speed))  # Clamp speed between 0-100
        duty = int(speed * self.max_duty / 100)
        self.motor_a.duty_u16(0)
        self.motor_b.duty_u16(duty)
    
    def stop(self):
        """Stop motor"""
        self.motor_a.duty_u16(0)
        self.motor_b.duty_u16(0)

# Example usage
def main():
    # Initialize motor driver with GPIO pins 16 and 17
    motor = L9110S(18, 19)
    
    while True:
        print("Forward at 50% speed")
        motor.forward(50)
        time.sleep(2)
        
        print("Stop")
        motor.stop()
        time.sleep(1)
        
        print("Backward at 75% speed")
        motor.backward(75)
        time.sleep(2)
        
        print("Stop")
        motor.stop()
        time.sleep(1)

if __name__ == '__main__':
    main()