import discord
import os
from dotenv import load_dotenv

''' a lot of these comments are gonna be redundant but it will help readability tbh '''


# load environment variables into os
load_dotenv()

# initialize client
client = discord.Client()

# callback for when bot is online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# callback for when bot receives a message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

# runs the bot with its login token
client.run(os.environ['TOKEN'])