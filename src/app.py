from discord.ext import commands
from os import getenv
import asyncio
import discord

from song_queue import SongQueue
from song import Song

TOKEN = getenv('API_TOKEN')
if TOKEN == None:
    raise EnvironmentError('Please set API_TOKEN environment variable.')

client = commands.Bot(command_prefix='.')


@client.command(brief='Plays a song by name or url',
                name="play",
                aliases=['p', 'resume', 'unpause', 'continue', 'PLAY'])
async def play(ctx, *, text=None):

    # Gets voice channel of message author
    author_voice_channel = ctx.author.voice
    if author_voice_channel is not None:
        voice_channel = author_voice_channel.channel
        try:
            global voice
            voice = await voice_channel.connect()
        except: pass
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
        return

    # If text is set/sent
    if text:
        # Keep donwloaded songs under 10
        Song.remove_older_files()

        # Creates empty queue
        global queue
        queue = SongQueue()

        song = Song(text)

        # Song is inappropriate when requires login
        if song.is_appropriate == False:
            await ctx.send("Youtube said this video is inappropriate.")
            return

        # Download song if doesn't already exists on dir
        song.download()

        queue.add_song(song)

        if voice.is_playing():
            # Sleep while audio is playing.
            while voice.is_playing():
                await asyncio.sleep(1)
            
            # Get and play next song in line if there is any
            next_song = queue.get_next_song()
            if next_song != None:
                voice.play(discord.FFmpegPCMAudio(next_song.file_path))

        # Runs the first time only
        else:
            next_song = queue.get_next_song()
            # print(next_song)
            voice.play(discord.FFmpegPCMAudio(next_song.file_path))
    
    # If text is not set resumes paused song
    else:
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")


@client.command(aliases=['stop'])
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def next(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# @client.command()
# async def current(ctx):
#     await ctx.send(f"Currently playing: {queue.current.title}")


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# Outputs on server terminal ready message
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(TOKEN)
