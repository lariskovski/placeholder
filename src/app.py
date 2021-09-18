from discord.ext import commands
from os import getenv, path, makedirs
import asyncio
import discord

from song_queue import SongQueue
from song import Song

TOKEN = getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


@client.command(brief='Plays a song by name or url',
                name="play",
                aliases=['p', 'resume', 'unpause', 'continue'])
async def play(ctx, *, text=None):

    # Create Downloads folder if not exists
    try:
        makedirs(Song.DOWNLOAD_DIR)
    except OSError as e:
        print(e)

    # Keep donwloaded songs under 10
    Song.remove_older_files()

    # Creates empty queue
    global queue
    queue = SongQueue()

    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        try:
            global voice
            voice = await voice_channel.connect()
        except: pass
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

    # If text is set/sent
    if text:
        song = Song(text)
        # Downloads song if it doesn't exist
        if not path.exists(song.file_path):
            song.download()
        queue.add_song(song)

        if voice.is_playing():
            # Sleep while audio is playing.
            while voice.is_playing():
                await asyncio.sleep(1)
            # print(queue.queue)
            next_song = queue.get_next_song()
            if next_song != None:
                voice.play(discord.FFmpegPCMAudio(next_song.file_path))

        # Runs the first time only
        else:
            next_song = queue.get_next_song()
            # print(next_song)
            voice.play(discord.FFmpegPCMAudio(next_song.file_path))
    
    # If paused, resumes
    else:
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")


@client.command()
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
