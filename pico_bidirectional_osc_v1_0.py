"""
Bidirectional OSC Communication for Raspberry Pi Pico W
Cross-Modal System Integration

Version: 1.0
Generated: January 21, 2026

Features:
- Creates WiFi hotspot
- Sends sensor data to computer
- Receives control commands from computer
- Works with Cross-Modal System via OSC bridge

Hardware: Pico W with sensors (temp, light, etc.)
"""

import network
from time import sleep, ticks_ms
import socket
from machine import ADC, Pin
from uosc.server import parse_message, parse_bundle
from uosc.client import Bundle, Client, create_message

# ===== Configuration =====
HOTSPOT_SSID = 'CrossModalPico'
HOTSPOT_PASSWORD = 'sensor2026'

LISTEN_PORT = 8000          # Pico listens for commands here
SEND_TO_IP = '192.168.4.2'  # Computer's IP (will get from first connection)
SEND_TO_PORT = 9001          # Send to bridge's OSC input port

SENSOR_UPDATE_RATE = 100     # Send sensor data every 100ms (10Hz)

# ===== WiFi Hotspot Setup =====
ap = network.WLAN(network.AP_IF)
ap.config(essid=HOTSPOT_SSID, password=HOTSPOT_PASSWORD)
ap.active(True)

while not ap.active():
    sleep(0.1)

print('=' * 50)
print('Pico Bidirectional OSC - v1.0')
print('Cross-Modal System Integration')
print('Generated: January 21, 2026')
print('=' * 50)
print('Pico WiFi Hotspot Active!')
print(f'SSID: {HOTSPOT_SSID}')
print(f'IP Address: {ap.ifconfig()[0]}')
print(f'Password: {HOTSPOT_PASSWORD}')
print('=' * 50)
print()

# ===== Sensor Setup =====
# Built-in temperature sensor
temp_sensor = ADC(4)

# Optional: External sensors
# light_sensor = ADC(26)  # Connect light sensor to GPIO26
# pot = ADC(27)           # Connect potentiometer to GPIO27

# Optional: LED for visual feedback
led = Pin('LED', Pin.OUT)

# ===== UDP Socket Setup =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', LISTEN_PORT))
sock.setblocking(False)

print(f"🎧 Listening for OSC on {ap.ifconfig()[0]}:{LISTEN_PORT}")
print(f"📤 Will send OSC to {SEND_TO_IP}:{SEND_TO_PORT}")
print()
print("Instructions:")
print("1. Connect computer to WiFi: 'CrossModalPico'")
print("2. Configure OSC bridge to send to 192.168.4.1:8000")
print("3. Pico will send sensor data automatically")
print('=' * 50)
print()

# ===== State Variables =====
last_sensor_send = ticks_ms()
computer_ip = None  # Will be set from first message received
led_brightness = 0  # Controlled from computer

# ===== Helper Functions =====

def read_temp():
    """Read internal temperature sensor (°C)"""
    reading = temp_sensor.read_u16()
    voltage = reading * 3.3 / 65535
    temp_c = 27 - (voltage - 0.706) / 0.001721
    return temp_c

def send_osc(address, *values):
    """Send OSC message to computer"""
    global computer_ip
    
    if computer_ip is None:
        # Use default IP until we know computer's IP
        target_ip = SEND_TO_IP
    else:
        target_ip = computer_ip
    
    try:
        # Create OSC message
        msg = create_message(address, values)
        sock.sendto(msg, (target_ip, SEND_TO_PORT))
    except Exception as e:
        print(f"Send error: {e}")

def send_sensor_data():
    """Send all sensor readings"""
    # Read sensors
    temp = read_temp()
    
    # Send temperature
    send_osc('/cms/input/thermal/pico/temperature', temp)
    
    # Optional: Send other sensors
    # light = light_sensor.read_u16() / 65535  # Normalize to 0-1
    # send_osc('/cms/input/vision/pico/light_level', light)
    
    # pot_value = pot.read_u16() / 65535
    # send_osc('/cms/input/control/pico/potentiometer', pot_value)
    
    # Heartbeat - blink LED
    led.toggle()

def handle_osc_command(address, args):
    """Process incoming OSC commands from computer"""
    global led_brightness, computer_ip
    
    print(f"📥 OSC IN: {address} {args}")
    
    # LED brightness control
    if address == '/cms/output/led/brightness':
        if args:
            led_brightness = args[0]
            # Control LED (0-1 range)
            if led_brightness > 0.5:
                led.on()
            else:
                led.off()
            print(f"   LED brightness: {led_brightness:.2f}")
    
    # Motor speed control (example)
    elif address == '/cms/output/motor/speed':
        if args:
            speed = args[0]
            print(f"   Motor speed: {speed:.2f}")
            # Add motor control code here
    
    # Generic output
    elif address.startswith('/cms/output/'):
        parts = address.split('/')
        if len(parts) >= 4 and args:
            output_type = parts[3]
            value = args[0]
            print(f"   {output_type}: {value:.2f}")

# ===== Main Loop =====
print("Starting main loop...")
print()

while True:
    current_time = ticks_ms()
    
    # === Send sensor data periodically ===
    if current_time - last_sensor_send >= SENSOR_UPDATE_RATE:
        send_sensor_data()
        last_sensor_send = current_time
    
    # === Receive OSC commands ===
    try:
        data, src = sock.recvfrom(1024)
        
        # Remember computer's IP from first message
        if computer_ip is None:
            computer_ip = src[0]
            print(f"✅ Computer connected from: {computer_ip}")
            print()
        
        try:
            # Parse OSC message
            if data.startswith(b'#bundle'):
                # Bundle with multiple messages
                for timetag, (addr, tags, args) in parse_bundle(data):
                    if not addr.startswith('/_'):
                        handle_osc_command(addr, args)
            else:
                # Single message
                addr, tags, args = parse_message(data)
                handle_osc_command(addr, args)
                
        except Exception as e:
            print(f"⚠️  Parse error: {e}")
        
    except OSError:
        # No data available (non-blocking socket)
        pass
    
    sleep(0.001)  # 1ms sleep to prevent busy waiting
