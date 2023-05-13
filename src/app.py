from discord.ext import commands
from os import getenv
import asyncio
import discord

from song_queue import SongQueue
from song import Song

TOKEN = getenv('API_TOKEN')
if TOKEN == None:
    raise EnvironmentError('Please set API_TOKEN environment variable.')

client = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Creates empty queue
global queue
queue = SongQueue()

@client.command(brief='Plays a song by name or url',
                name="play",
                aliases=['p', 'PLAY'])
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
        song = Song(text)

        # Song is inappropriate when requires login
        if song.is_appropriate == False:
            await ctx.send("Youtube flagged the song as inappropriate. Can't play it.")
            return

        # Download song if doesn't already exists on dir
        song.download()

        queue.add_song(song)
        await ctx.send(f"Added {song.title} to queue.")

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
        await ctx.send("Tell me a song to play.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send("Stopped and cleared queue.")
    else:
        await ctx.send("No audio is playing.")


@client.command()
async def next(ctx):
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
    
    # Get and play next song in line if there is any
    next_song = queue.get_next_song()
    if next_song != None:
        voice.stop()
        voice.play(discord.FFmpegPCMAudio(next_song.file_path))
        await ctx.send(f"Now playing: {queue.current.title}")
    else:
        await ctx.send("No more songs in queue.")


@client.command()
async def current(ctx):
    await ctx.send(f"Playing: {queue.current.title}")


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# Outputs on server terminal ready message
@client.event
async def on_ready():
    print(f'We have logged in as {client.user} and are ready to play music!')

client.run(TOKEN)
