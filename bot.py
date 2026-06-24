#pip install -U discord.py

import serial
import tty
import sys
import termios
import signal
import time

import os
import discord
from dotenv import load_dotenv

#import ollama
import re
import asyncio


# try:
#     arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# except:
#     arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

arduino = serial.Serial('/dev/cu.usbmodem11301', 9600, timeout=1)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
	print("we exist!")
	print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
	print("message has been sent")
	print(message.content)
	matches = re.findall(r"(?:\"[^\"]*\"|'[^']*'|\*([^*]+)\*)", message.content)
	print(matches)
	parse_command(message.author, matches)
	if message.author in ai_authors:
		matches = re.findall(r"(?:\"[^\"]*\"|'[^']*'|\*([^*]+)\*)", message.content)
		print(matches)
		

def parse_command(ai_author, commands):
	for command in commands:
		print(f"command in commands {command}")
		if command in moves_library:
			print(moves_library[command])
			send_commands(ai_author, moves_library[command])
		
		
	# try:		
	# 	if command[1][-1] == ";":
	# 		command = command[:-1]
	# 	#command = [joint_name: move_name; joint_name: move_name]
	# 	commands = command.split("; ")
	# 	# commands = [joint_name: move_name, joint_name: move_name]
				
	# 	for joint in commands:
	# 		# joint = [joint_name: move_name]
	# 		joint_name, move_name = joint.split(": ")
			
	# 		try:
	# 			angle = joint_commands[joint_name][move_name]
	# 			joint = (f"{joint_name}: {angle}")
	# 			print(joint)
	# 			print(commands)
	# 		except:
	# 			raise Exception(f"Unknown: {joint_name}: {move_name}")
	# 		finally: 
	# 			send_commands(ai_author, commands)
				
	# finally:
	# 	arduino.close()
	# 	print("Disconnected.")


def send_commands(ai_author, commands):
	#do not use ai_author since we have only 1 arduino
	
	#send comands individually 
	#cause arduino doesn't have additional power source
	#and will break trying to move multiple servo's at once
	for msg in commands: 
		message = str(msg)
		message = message[1:-1]
		message += "\n"
		print(message)
		arduino.write(message.encode())
		time.sleep(0.3)


moves_library = {
	"rest":[
		{"elbow_l": 0},
		{"shoulder_l_reach": 0},
		{"shoulder_l_lift": 0},
		{"elbow_r": 0},
		{"shoulder_r_reach": 0},
		{"shoulder_r_lift": 0},
	],
	"flex_arm":[
		{"shoulder_l_reach": 90},
		{"elbow_l": 180},
		{"elbow_l": 0},
		{"elbow_l": 90},
		{"elbow_l": 180},
		{"elbow_l": 0},
	],
	"shake_hand": [
		{"shoulder_l_reach": 90},
		{"shoulder_l_reach": 80},
		{"shoulder_l_reach": 100},
		{"shoulder_l_reach": 80},
		{"shoulder_l_reach": 100},
		{"shoulder_l_reach": 90},
	],
	"wave_over": [
		{"shoulder_l_lift": 165},
		{"shoulder_l_lift": 135},
		{"shoulder_l_lift": 165},
		{"shoulder_l_lift": 135},
		{"shoulder_l_lift": 165},
	],
}


ai_authors = ["names of all of the ai's talking"]

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


client.run(TOKEN)
