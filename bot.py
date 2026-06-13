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

import ollama
import re


try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

# .env
# DISCORD_TOKEN={your-bot-token}
#pip install -U python-dotenv


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author in ai_authors:
		joint_commands = []
		matches - re.findall(r'\*([^*]+)\*', message.content)
		
		for expression in matches:
			print(f"Expression detected: {expression}")
				response = await asyncio.to_thread(
					ollama.chat,
					model = "llama3.2",
					messages = [
						{"role": "system", "content": "my super cool and awesome system prompt"},
						{"role", "user", "content": expression},
				]
			)

			print(f"Joint command: {message.author}: {command}")
			parse_command(message.author, response['message']['content'])


def parse_command(ai_author, command):
	try:		
		if command[1][-1] == ";":
			command = command[:-1]
		#command = [joint_name: move_name; joint_name: move_name]
		commands = command.split("; ")
		# commands = [joint_name: move_name, joint_name: move_name]
				
		for joint in commands:
			# joint = [joint_name: move_name]
			joint_name, move_name = joint.split(": ")
			
			try:
				angle = joint_commands[joint_name][move_name]
				joint = (f"{joint_name}: {angle}")
				print(joint)
				print(commands)
			except:
				raise Exception(f"Unknown: {joint_name}: {move_name}")
			finally: 
				send_commands(author, commands)
				
	finally:
		arduino.close()
		print("Disconnected.")


def send_commands(ai_author, commands):
	#do not use ai_author since we have only 1 arduino
	
	#send comands individually 
	#cause arduino doesn't have additional power source
	#and will break trying to move multiple servo's at once
	for message in commands: 
		message += "\n"
		print(message)
		arduino.write(message.encode())
		time.sleep(0.5)



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





      
    
    
