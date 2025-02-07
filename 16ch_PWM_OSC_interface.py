import utime as time
import network
import socket
from ustruct import unpack
from machine import Pin, PWM

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(wlan.scan())
wlan.connect('DNA-WIFI-9CC7', '54108537')
#wlan.connect('FASTWEB-1-D3F359', '97BF570AC7')
#wlan.connect('TP-Link_6CEE', '13042905')

while not wlan.isconnected() and wlan.status() >= 0:
    print('Waiting for connection...')
    time.sleep(1)
print('WLAN connection state:', wlan.status())
print('WLAN ifconfig:', wlan.ifconfig())
print('IP address:', wlan.ifconfig()[0])

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

def get_hostport(addr):
    if isinstance(addr, tuple):
        return addr
    af, addr, port = socket.sockaddr(addr)
    return inet_ntop(af, addr), port

def decode_osc(data):
    reader_pos = 0
    path_end = data.find(b'\0', reader_pos)
    path = data[reader_pos:path_end].decode('utf-8')
    #print("p", reader_pos, path_end, path);
    
    reader_pos = (path_end + 4) & ~0x03
    oformat_end = data.find(b'\0', reader_pos)
    oformat = data[reader_pos:oformat_end].decode('utf-8')
    #print("f", reader_pos, oformat_end, oformat);
    
    reader_pos = (oformat_end + 4) & ~0x03
    value = unpack('>ffffffffffffffff', data[reader_pos:reader_pos+64])
    #print("v", reader_pos, value);
    return True, path, value

so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    print(so)
    DEFAULT_ADDRESS = wlan.ifconfig()[0]
    DEFAULT_PORT = 9001
    MAX_DGRAM_SIZE = 1472
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ai = socket.getaddrinfo(DEFAULT_ADDRESS, DEFAULT_PORT)[0]
    so.bind(ai[-1])
    print("Listening for OSC messages on:", ai[-1])

    while True:
        data, caddr = so.recvfrom(MAX_DGRAM_SIZE)
#         print("received: ", len(data), *get_hostport(caddr))
        
        ok, path, value = decode_osc(data)
        if ok:
            if path == '/pwm':
                for i in range(16):
                    set_pwm(i, int(value[i]))
#         print(path)
        print(value)

finally:

    for pin in range(16):
        pwm_objects[pin].deinit()
    so.close()
    print('closing')



