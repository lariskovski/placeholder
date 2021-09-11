from youtube_search import YoutubeSearch
import youtube_dl
import json
import os


def search_song(text):
    # Check if input is already url format
    if "http" in text:
        song = text
    # If not search for keywords on youtube
    else:
        video_search = YoutubeSearch(song, max_results=1).to_json()
        video_id = str(json.loads(video_search)['videos'][0]['id'])
        print(str(json.loads(video_search)['videos']))
        song = 'https://www.youtube.com/watch?v='+ video_id    
    return song


def download_song(song: str, file_path=None) -> None:
    # if file_path == None:
    #     file_path = f"{os.path.abspath(os.getcwd())}/song.mp3"

    # Check if file exists if does, removes it
    # song_there = os.path.isfile(file_path)
    # try:
    #     if song_there:
    #         os.remove(file_path)
    # except PermissionError:
    #     print("Wait for the current playing song to end or use the 'stop' command")
    #     return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    song_url = search_song(song)

    # Downloads audio file from youtube then plays it
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])
