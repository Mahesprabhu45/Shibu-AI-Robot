import serial
import serial.tools.list_ports
import time

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if ("USB" in p.device) or ("ACM" in p.device):
            return p.device
    return None

def send_command(cmd):
    port = find_arduino()
    if not port:
        print("? Arduino not found!")
        return
    
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)
    ser.write((cmd + "\n").encode())
    print(f"? Sent command: {cmd}")
    ser.close()

# Send Right
send_command("R")
