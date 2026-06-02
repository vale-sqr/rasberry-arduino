import serial
import tty
import sys
import termios
import signal

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)  # Always restore terminal
    return key

print("Controls: A/D = Servo1, W/S = Servo2, C = Center, Q or ^C = Quit")

try:
    while True:
        key = get_key().lower()
        if key in ('q', '\x03'):  # \x03 is Ctrl+C in raw mode
            break
        if key in ('a', 'd', 'w', 's', 'c'):
            arduino.write(key.encode())
            print(f"Sent: {key}")
finally:
    arduino.close()
    print("Disconnected.")