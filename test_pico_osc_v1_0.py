#!/usr/bin/env python3
"""
Test Pico OSC Communication
Simple script to verify Pico bidirectional OSC is working

Version: 1.0
Generated: January 21, 2026

Usage:
1. Connect to Pico WiFi hotspot (CrossModalPico)
2. Run: python3 test_pico_osc.py
3. Should see temperature updates from Pico
4. Press 'l' + Enter to toggle LED
"""

import socket
import time
from pythonosc import udp_client, dispatcher, osc_server
import threading

# Configuration
PICO_IP = "192.168.4.1"
PICO_PORT = 8000

LISTEN_PORT = 9001

# OSC client to send to Pico
osc_client = udp_client.SimpleUDPClient(PICO_IP, PICO_PORT)

# LED state
led_on = False

def handle_osc_message(address, *args):
    """Print received OSC messages from Pico"""
    print(f"📥 FROM PICO: {address} {args}")
    
    if address == '/cms/input/thermal/pico/temperature' and args:
        temp = args[0]
        print(f"   🌡️  Temperature: {temp:.2f}°C")

def start_osc_receiver():
    """Start OSC receiver in background thread"""
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(handle_osc_message)
    
    server = osc_server.ThreadingOSCUDPServer(
        ("0.0.0.0", LISTEN_PORT), disp
    )
    
    print(f"🎧 Listening for Pico on port {LISTEN_PORT}")
    
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    
    return server

def send_led_command(value):
    """Send LED brightness command to Pico"""
    osc_client.send_message('/cms/output/led/brightness', value)
    print(f"📤 TO PICO: /cms/output/led/brightness {value}")

def main():
    print("=" * 60)
    print("Pico OSC Communication Test")
    print("=" * 60)
    print()
    print("Make sure:")
    print("1. Computer is connected to 'CrossModalPico' WiFi")
    print("2. Pico code is running (main.py)")
    print("3. Your IP should be 192.168.4.2")
    print()
    print(f"Pico address: {PICO_IP}:{PICO_PORT}")
    print()
    
    # Check network
    try:
        import subprocess
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        if '192.168.4.2' in result.stdout:
            print("✅ Connected to Pico network (192.168.4.2)")
        else:
            print("⚠️  Not connected to Pico network!")
            print("   Connect to 'CrossModalPico' WiFi first")
            return
    except:
        print("⚠️  Can't verify network (run 'ifconfig' manually)")
    
    print()
    print("=" * 60)
    print("Starting test...")
    print("=" * 60)
    print()
    
    # Start receiver
    server = start_osc_receiver()
    
    print("Commands:")
    print("  l = Toggle LED")
    print("  b = Set LED brightness (0-1)")
    print("  t = Send test message")
    print("  q = Quit")
    print()
    print("Listening for Pico sensor data...")
    print("(You should see temperature updates every 100ms)")
    print()
    
    global led_on
    
    try:
        while True:
            cmd = input().strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'l':
                led_on = not led_on
                send_led_command(1.0 if led_on else 0.0)
                print(f"LED: {'ON' if led_on else 'OFF'}")
            elif cmd == 't':
                send_led_command(0.5)
                print("Sent test brightness: 0.5")
            elif cmd.startswith('b '):
                try:
                    value = float(cmd.split()[1])
                    value = max(0.0, min(1.0, value))
                    send_led_command(value)
                    print(f"Sent brightness: {value}")
                except:
                    print("Usage: b 0.5")
            else:
                print("Unknown command")
    
    except KeyboardInterrupt:
        print("\n\nStopping...")
    
    print("\n✅ Test complete")

if __name__ == "__main__":
    main()
