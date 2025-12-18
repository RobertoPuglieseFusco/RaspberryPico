import network
from time import sleep
import socket
from uosc.server import parse_message, parse_bundle

# ===== WiFi Hotspot =====
ap = network.WLAN(network.AP_IF)
ap.config(essid='HypoxiaControl', password='hypoxia2024')
ap.active(True)

while not ap.active():
    sleep(0.1)

print('=' * 40)
print('Hotspot Active!')
print(f'IP: {ap.ifconfig()[0]}')
print('=' * 40)

# ===== UDP Socket =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8000))
sock.setblocking(False)

print(f"OSC listening on {ap.ifconfig()[0]}:8000")
print()

# ===== Main Loop =====
while True:
    try:
        data, src = sock.recvfrom(1024)
        
        try:
            # Check if bundle or single message
            if data.startswith(b'#bundle'):
                for timetag, (addr, tags, args) in parse_bundle(data):
                    if not addr.startswith('/_'):
                        print(f"OSC: {addr}")
                        print(f"Args: {args}")
                        print(f"Number of values: {len(args)}")
                        
                        # Access individual values
                        if args:
                            print(f"First value: {args[0]}")
                            print(f"All values: {list(args)}")
                        
                        print("-" * 30)
            else:
                addr, tags, args = parse_message(data)
                #print(f"OSC: {addr}")
                #print(f"Args: {args}")
                #print(f"Number of values: {len(args)}")
                
                #if args:
                    #print(f"First value: {args[0]}")
                    #print(f"All values: {list(args)}")
                
                #print("-" * 30)
                
                if addr == '/test':
                    values = list(args)
                    for i, val in enumerate(values):
                        print(f"Value {i}: {val}")
                
        except Exception as e:
            print(f"Parse error: {e}")
        
    except OSError:
        pass
    
    sleep(0.001)