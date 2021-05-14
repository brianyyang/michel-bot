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

#################### FLAGS TO KEEP TRACK OF ####################################################


jocey_react_flag = True


#################### MAIN CALLBACKS ############################################################


# callback for when bot is online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# callback for when bot receives a message
@client.event
async def on_message(message):
    # ignore if I sent the message
    if message.author == client.user:
        return

    # check if message is a command
    if message.content.startswith('!'):
        await handle_command(message, message.content[1:])

    # see helper function below
    if jocey_react_flag:
        await scary_jocey_react(message)


##################### HELPER FUNCTIONS #########################################################


# say hello - demo function
async def send_hello(message):
    await message.channel.send('Hello!')


# toggles whether or not I am reacting to messages relating to jocelyn
async def toggle_jocey_react(message):
    global jocey_react_flag
    jocey_react_flag = not jocey_react_flag
    await message.channel.send('Toggled Jocelyn reacts.')


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


# dictionary that holds commands and their respective functions
command_switcher = {
    'hello': send_hello,
    'jocey': toggle_jocey_react
}


# delegate command to the correct helper
async def handle_command(message, command):
    await command_switcher[command](message)


################################################################################################


# runs the bot with its login token
client.run(os.environ['TOKEN'])