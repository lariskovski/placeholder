from youtube_dl import YoutubeDL
from requests import get


class Song:
    DOWNLOAD_DIR = 'downloads'

    def __init__(self, arg) -> None:
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

        self.title = video['title']
        self.hashed_title = self.hash_title()
        self.url = video['webpage_url']
        self.file_path = f'{self.DOWNLOAD_DIR}/{self.hashed_title}.mp3'


    def download(self) -> str:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.file_path,
            'noplaylist':'True',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    
    def hash_title(self) -> str:
        import hashlib
        hash = int(hashlib.sha256(self.title.encode('utf-8')).hexdigest(), 16) % 10**8
        return str(hash)


    @classmethod
    def remove_older_files(cls) -> None:
        import os
        files_in_dir: list = os.listdir(cls.DOWNLOAD_DIR)
        full_path : list= [f"{cls.DOWNLOAD_DIR}/{file}" for file in files_in_dir]

        if len(files_in_dir) >= 10:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)

