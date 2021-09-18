from youtube_dl import YoutubeDL
from requests import get
import youtube_dl


DOWNLOAD_DIR = 'downloads'


def hash_title(title) -> str:
    import hashlib
    hash = int(hashlib.sha256(title.encode('utf-8')).hexdigest(), 16) % 10**8
    return str(hash)


def remove_older_files() -> None:
    import os
    # downloads_dir = f"{os.path.abspath(os.getcwd())}/{DOWNLOAD_DIR}"
    files_in_dir: list = os.listdir(DOWNLOAD_DIR)
    full_path : list= [f"{DOWNLOAD_DIR}/{file}" for file in files_in_dir]

    if len(files_in_dir) >= 10:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)


def get_song_info(arg) -> dict:
    ydl_opts = {
        'format': 'bestaudio/best',
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
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
        # print(f"[log] title: {video['title']}")

        return {'title': video['title'],
                'url': f"https://www.youtube.com/watch?v={video['id']}"}


def download_song(song: str) -> str:
    remove_older_files()

    song_info = get_song_info(song)
    
    title = f"{hash_title(song_info['title'])}.mp3"
    file_path =  f'{DOWNLOAD_DIR}/{title}'

    # 'outtmpl': '%(title)s.%(ext)s'
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

    song_url = song_info['url']

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])

    return file_path


if __name__ == "__main__":
    download_song('https://www.youtube.com/watch?v=9gsAz6S_zSw')
