from requests import get
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
from discord.ext import commands
# from time import sleep
import discord
import os

from downloader import download_song

TOKEN = os.getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


def delete_file(file_path):
    # Check if file exists if does, removes it
    song_there = os.path.isfile(file_path)
    try:
        if song_there:
            os.remove(file_path)
    except PermissionError:
        return


def download_file(arg, file_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'noplaylist':'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
    print(f"Title: {video['title']} Id:{video['id']}")


@client.command(brief='This command plus an audio name, plays it',
                name="play")
async def play(ctx, *, text):
    import asyncio
    file_path = f"{os.path.abspath(os.getcwd())}/song.mp3"
    delete_file(file_path)

    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        try:
            global voice
            voice = await voice_channel.connect()
        except: pass
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    if not voice.is_playing():
        song = download_file(text, file_path)
        voice.play(discord.FFmpegPCMAudio(file_path))
        # Sleep while audio is playing.
        while voice.is_playing():
            await asyncio.sleep(1)
        await ctx.voice_client.disconnect()
    else:
        print('Music is already playing')


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# Outputs on server terminal ready message
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(TOKEN)
