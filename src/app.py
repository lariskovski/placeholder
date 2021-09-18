from discord.ext import commands
import discord
import os

from downloader import download_song
from queue_mgmt import SongQueue

TOKEN = os.getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


@client.command(brief='This command plus an audio name, plays it',
                name="play")
async def play(ctx, *, text=None):
    import asyncio

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

    # If paused, resumes
    if text == None:
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    song = download_song(text)
    queue.add_song(song)

    if voice.is_playing():
        # Sleep while audio is playing.
        while voice.is_playing():
            await asyncio.sleep(1)
        # await ctx.voice_client.disconnect()
        print(queue.queue)
        next_song = queue.get_next_song()
        if next_song != None:
            voice.play(discord.FFmpegPCMAudio(next_song))
    
    # runs the first time
    else:
        next_song = queue.get_next_song()
        voice.play(discord.FFmpegPCMAudio(next_song))


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


@client.command()
async def current(ctx):
    await ctx.send(queue.current)


# Outputs on server terminal ready message
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(TOKEN)
