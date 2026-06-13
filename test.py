import serial
import tty
import sys
import termios
import signal
import time

joint_commands = {
    'neck_nod': 
        {
            'up': 0, 
            'up_soft': 45, 
            'forward': 90, 
            'down_soft': 135, 
            'down': 180
        }, 
    'neck_turn': 
        {
            'left': 0, 
            'left_soft': 45, 
            'neutral': 90, 
            'right_soft': 135, 
            'right': 180
        },
    'neck_roll': 
        {
            'left': 0, 
            'left_soft': 45, 
            'neutral': 90, 
            'right_soft': 135, 
            'right': 180
        },
    'shoulder_l_reach': 
        {
            'up': 180, 
            'forward_raised': 135, 
            'forward': 90, 
            'forward_lowered': 45, 
            'down': 0,
        },
    'shoulder_l_lift': 
        {
            'down': 0, 
            'lowered': 45, 
            'side': 90, 
            'raised': 135, 
            'up': 180
        },
    'shoulder_r_reach': 
        {
            'up': 0, 
            'forward_raised': 45, 
            'forward': 90, 
            'forward_lowered': 135, 
            'down': 180,
        },
    'shoulder_r_lift': 
        {
            'down': 0, 
            'lowered': 45, 
            'side': 90, 
            'raised': 135, 
            'up': 180
        },
    'elbow_l': 
        {
            'open': 0, 
            'open_slight': 45, 
            'right_angle': 90, 
            'bent': 135, 
            'closed': 180
        },
    'elbow_r': 
        {
            'open': 0, 
            'open_slight': 45, 
            'right_angle': 90, 
            'bent': 135, 
            'closed': 180
        }
}

try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=1)



# library joint: {move: degree}

try:
    while True:
        print("Write commands in [joint]: '[move]; [joint]: [move]; format'")
        command = input("Movement: ")
        # shoulder_left_side_rise: up; elbow_left: full_open
        if command[-1] == ";":
            command = command[:-1]
        
        
        commands = command.split("; ")
        # commands = [joint: move, joint: move]

        parts = []

        for joint in commands:
            # joint = [joint, move]
            joint_name, move_name = joint.split(": ")

            try:
                angle = joint_commands[joint_name][move_name]
                parts.append(f"{joint_name}:{angle}")
                print(parts)
            except:
                raise Exception(f"Unknown: {joint_name}: {move_name}")
            finally: 
                for message in parts: 
                    #send comands individually 
                    #cause arduino doesn't have additional power source
                    #and will break trying to move multiple servo's at once
                    message += "\n"
                    print(message)
                    arduino.write(message.encode())
                    time.sleep(0.5)


finally:
    arduino.close()
    print("Disconnected.")
