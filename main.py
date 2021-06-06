import discord
from discord.ext import commands, tasks
import os
import youtube_dl
from youtube_dl.utils import DownloadError 
# if ran locally
from dotenv import load_dotenv

''' a lot of these comments are gonna be redundant but it will help readability tbh '''

# if ran locally
# load environment variables into os 
load_dotenv()

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

# initialize bot client 
bot = commands.Bot(command_prefix='?', help_command=help_command)

#################### GLOBALS TO KEEP TRACK OF ####################################################


jocey_react_flag = False


#################### MAIN CALLBACKS ############################################################


# callback for when bot is online
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# callback for when bot receives a message
@bot.event
async def on_message(message):
    # ignore if I sent the message
    if message.author == bot.user:
        return

    # see helper function below
    if jocey_react_flag:
        await scary_jocey_react(message)

    # check if the user inputted a command and perform it if so
    await bot.process_commands(message)


##################### COMMANDS #################################################################


# say hello - demo command
@bot.command(name='hello', help='Demo command, tells me to say hi.')
async def send_hello(ctx):
    await ctx.message.channel.send('Hello!')


# toggles whether or not I am reacting to messages relating to jocelyn
@bot.command(name='jocey', help='Toggles Jocelyn reacts on appropriate messages.')
async def toggle_jocey_react(ctx):
    global jocey_react_flag
    jocey_react_flag = not jocey_react_flag
    await ctx.message.channel.send('Toggled Jocelyn reacts.')


# joins voice to presumably start playing audio
@bot.command(name='join', help='Tells me to join you in your voice channel.')
async def join_voice(ctx):
    user = ctx.message.author
    if not user.voice:
        await ctx.send(f'<@{user.id}>, you are not connected to a voice channel.')
        return
    if ctx.message.guild.voice_client and ctx.message.guild.voice_client.is_connected():
        await ctx.send(f'<@{user.id}>, I\'m already in a voice channel.')
        return
    await user.voice.channel.connect()


# leaves the voice channel I'm currently in
@bot.command(name='leave', help=f'Tells me to leave the voice channel I\'m in.')
async def leave_voice(ctx):
    if ctx.message.guild.voice_client and ctx.message.guild.voice_client.is_connected():
        await ctx.message.guild.voice_client.disconnect()
    else:
        await ctx.send(f'<@{ctx.message.author.id}>, I\'m not connected to a voice channel.')


# queues a video to play from youtube
@bot.command(name='play', help='Plays the song from youtube from the given URL.')
async def play_song(ctx, url):
    try:
        # find and download the mp3 from the video
        downloader = youtube_dl.YoutubeDL({'format': 'bestaudio', 'title': True})
        extracted_info = downloader.extract_info(url, download=False)
        # play the song
        ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url']))
    except DownloadError:
        await ctx.send(f'<@{ctx.message.author.id}>, you gave me an invalid URL.')
    except AttributeError:
        await ctx.send(f'<@{ctx.message.author.id}>, I\'m not connected to a voice channel.')


# stops the curent song that is playing
@bot.command(name='stop', help='Ends the currently playing song.')
async def stop_song(ctx):
    ctx.message.guild.voice_client.stop()


##################### HELPER FUNCTIONS #########################################################


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
bot.run(os.environ['TOKEN'])