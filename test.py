import serial
import tty
import sys
import termios
import signal
from joint_library import joint_commands

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

#print("Controls: A/D = Servo1, W/S = Servo2, C = Center, Q or ^C = Quit")

# library joint: {move: degree}

try:
    while True:
        print("Write commands in [joint]: [move]; [joint]: [move]; format")
        command = input("Movement: ")
        # shoulder_left_side_rise: up; elbow_left: full_open
        if command[-1] == ";"
            command = command[:-1]
        
        commands = command.split("; ")
        # commands = [joint: move, joint: move]

        for joint in commands:
            # joint = [joint, move]
            joint_name, move_name = joint.split(": ")

            try:
                angle = joint_command[joint_name][joint_move]
                parts.append(f"{joint_name}:{angle}")
            except:
                raise Exception(f"Unknown: {joint_name}: {move_name}")
            finally: 
                 message = ",".join(parts) + "\n"
                arduino.write(message.encode())




            # try:
            #     joint_moves = joint_commands[joint_name]
            #     # joint_moves = {move: degree, move: degree, move: degree, move: degree}
            #     try: 
            #         angle = joint_moves[move_name]
            #         # angle = degree
            #     except:
            #         raise Exception(f"{move_name} is not part of {joint_name} move library")
            # except: 
            #     raise Exception(f"{joint_name} is not one of the available joints")
            # else:
            #     arduino.write(f"{joint_name}:{angle}\n".encode())
            #     print(f"Sent: {joint_name}: {joint_move}")
        
        # key = get_key().lower()
        # if key in ('q', '\x03'):  # \x03 is Ctrl+C in raw mode
        #     break
        # if key in ('a', 'd', 'w', 's', 'c'):
        #     arduino.write(key.encode())
        #     print(f"Sent: {key}")
        
finally:
    arduino.close()
    print("Disconnected.")
