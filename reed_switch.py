from machine import Pin, Timer
import time

# Initialize reed sensor and LED
reed = Pin(16, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

# Variables for speed calculation
last_state = reed.value()
last_edge_time = 0
current_rpm = 0
rotation_times = []  # Store the last few rotation times for averaging
max_samples = 5      # Number of samples to average

def calculate_rpm():
    global rotation_times, current_rpm
    
    # If we have no measurements, return 0
    if len(rotation_times) == 0:
        current_rpm = 0
        return
    
    # Calculate average time per rotation
    avg_rotation_time = sum(rotation_times) / len(rotation_times)  
    
    # Convert to RPM (60000 ms in a minute)
    current_rpm = 60000 / avg_rotation_time if avg_rotation_time > 0 else 0
    
    # Only print if there's actual movement detected
    if current_rpm > 0:
        print(f"Speed: {current_rpm:.1f} RPM")

def check_timeout():
    global rotation_times, current_rpm
    
    # If no new edge detected in 2 seconds, assume speed is 0
    current_time = time.ticks_ms()
    if rotation_times and time.ticks_diff(current_time, last_edge_time) > 2000:
        rotation_times = []
        if current_rpm > 0:  # Only print if we're changing from non-zero
            current_rpm = 0
            print("Speed: 0.0 RPM")

def reed_callback(pin):
    global last_state, last_edge_time, rotation_times
    
    # Get current time and state
    current_time = time.ticks_ms()
    current_state = pin.value()
    
    # Debounce (ignore transitions that happen too quickly)
    if time.ticks_diff(current_time, last_edge_time) < 5:  # 5ms debounce
        return
    
    # Update LED
    if current_state == 0:  # Magnet detected
        led.on()
    else:
        led.off()
    
    # If this is a falling edge (1->0, magnet arriving)
    if current_state == 0 and last_state == 1:
        # If we have a previous falling edge time, calculate the full rotation period
        if last_edge_time > 0:
            period = time.ticks_diff(current_time, last_edge_time)
            
            # Add to our samples
            rotation_times.append(period)
            
            # Keep only the most recent samples
            if len(rotation_times) > max_samples:
                rotation_times.pop(0)
            
            # Calculate and display the current RPM
            calculate_rpm()
        
        # Update last edge time
        last_edge_time = current_time
    
    # Update last state
    last_state = current_state

def timer_callback(timer):
    check_timeout()

def main():
    # Set up interrupt for reed sensor
    reed.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=reed_callback)
    
    # Set up timer for timeout checking
    timer = Timer()
    timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)
    
    try:
        while True:
            # Main loop - everything happens in callbacks
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Clean up
        timer.deinit()
        print("Program stopped")

if __name__ == "__main__":
    main()