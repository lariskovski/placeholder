from youtube_search import YoutubeSearch
from discord.ext import commands
import youtube_dl
import os, json
import discord
from time import sleep

TOKEN = os.getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


def get_url(song):
    video_search = YoutubeSearch(song, max_results=1).to_json()
    video_id = str(json.loads(video_search)['videos'][0]['id'])
    return 'https://www.youtube.com/watch?v='+ video_id


def download_song(song, file_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    # Check if input is already url format
    # If not search for keywords on youtube
    # and return url
    if "http" in song:
        url = song
    else:
        url = get_url(song)

    # Downloads audio file from youtube
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@client.command(brief='This command plus an audio name, plays it',
                name="play",
                aliases=['p'])
async def play(ctx, *, message):
    file_path = f"{os.path.abspath(os.getcwd())}/song.mp3"

    # Check if file exists if does, removes it
    song_there = os.path.isfile(file_path)
    try:
        if song_there:
            os.remove(file_path)
    except PermissionError:
        await ctx.send("Wait for the current playing song to end or use the 'stop' command")
        return

    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect()

    download_song(message, file_path=file_path)

    vc.play(discord.FFmpegPCMAudio(file_path))
    # while vc.is_playing():
    #         sleep(.1)
    # await vc.disconnect()

    # Delete command after the audio is done playing.
    await ctx.message.delete()


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


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
