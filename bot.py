pip install -U discord.py

import os
import discord
from dotenv import load_dotenv

import ollama
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.CLIENT()

# .env
# DISCORD_TOKEN={your-bot-token}
#pip install -U python-dotenv

ai_authors = ["names of all of the ai's talking"]

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author in ai_authors:
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
    
        joint_commnd = response['message']['content'] 
        print(f"Joint commands: {joint_command}")
          #format how I need to send the message






      
    
    
