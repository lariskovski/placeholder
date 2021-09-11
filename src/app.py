from youtube_search import YoutubeSearch
from discord.ext import commands
import youtube_dl
import os, json
import discord
from time import sleep

TOKEN = os.getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


@client.command(brief='This command plus an audio name, plays it',
                name="play")
async def play(ctx, *, message):
    filename = "song.mp3"

    # Check if file exists if does, removes it
    song_there = os.path.isfile(filename)
    try:
        if song_there:
            os.remove(filename)
    except PermissionError:
        await ctx.send("Wait for the current playing song to end or use the 'stop' command")
        return

    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    # Check if input is already url format
    if "http" in message:
        song = message
    # If not search for keywords on youtube
    else:
        video_search = YoutubeSearch(message, max_results=1).to_json()
        video_id = str(json.loads(video_search)['videos'][0]['id'])
        song = 'https://www.youtube.com/watch?v='+ video_id

    # Downloads audio file from youtube then plays it
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song])

    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, filename)

    vc.play(discord.FFmpegPCMAudio(filename))
    while vc.is_playing():
            sleep(.1)
    await vc.disconnect()

    # Delete command after the audio is done playing.
    await ctx.message.delete()


# Outputs on server terminal ready message
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(TOKEN)
