from discord.ext import commands
from time import sleep
import discord
import os

from downloader import download_song

TOKEN = os.getenv('API_TOKEN')
client = commands.Bot(command_prefix='.')


@client.command(brief='This command plus an audio name, plays it',
                name="play",
                aliases=['p'])
async def play(ctx, *, message):

    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect()

    download_song(song=message)
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
