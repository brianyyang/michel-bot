import discord
import os
# if ran locally
# from dotenv import load_dotenv 

''' a lot of these comments are gonna be redundant but it will help readability tbh '''

# if ran locally
# load environment variables into os 
# load_dotenv()

# initialize client
client = discord.Client()

#################### MAIN CALLBACKS ###################

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

    await scary_jocey_react(message)

##################### HELPER FUNCTIONS ##################

# determines if i should react to jocelyn's message with the scaryjocey emote
async def scary_jocey_react(message):
    source = message.author
    if f'{source.name}#{source.discriminator}' == 'jocelyn#5644' or 'jocelyn' in message.content.lower():
        scary_jocey_emote = await get_emoji('scaryjocey', message.guild)
        await message.add_reaction(scary_jocey_emote)

# finds a custom emoji on the server and returns it
async def get_emoji(emoji_name, guild):
     emoji_list = guild.emojis
     for emoji in emoji_list:
         if emoji.name == emoji_name:
             return emoji


# runs the bot with its login token
client.run(os.environ['TOKEN'])