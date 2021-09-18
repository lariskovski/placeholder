from youtube_dl import YoutubeDL
from requests import get
import youtube_dl

from songs import Song


def download_song(song: Song) -> str:

    # 'outtmpl': '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': song.file_path,
        'noplaylist':'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song.url])


if __name__ == "__main__":
    download_song('https://www.youtube.com/watch?v=9gsAz6S_zSw')
