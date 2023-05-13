from yt_dlp import YoutubeDL, utils
import os

class Song:
    DOWNLOAD_DIR: str = 'downloads'

    def __init__(self, arg) -> None:
        self.is_appropriate: bool = True
        self.info: dict = self.collect_info(arg)

        self.url: str = self.info['webpage_url'] if self.is_appropriate else None
        self.title: str = self.info['title'] if self.is_appropriate else None
        self.hashed_title: str = self.hash_title() if self.is_appropriate else None
        self.file_path: str = f'{self.DOWNLOAD_DIR}/{self.hashed_title}.mp3' if self.is_appropriate else None


    def collect_info(self, arg)-> dict:
        ydl_opts: dict = {
                            'format': 'bestaudio/best',
                            'noplaylist':'True',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192'
                            }],
                         }
    
        with YoutubeDL(ydl_opts) as ydl:
            hyperlink: bool = False

            if 'youtube.com' in arg:
                hyperlink = True
            
            try:
                if hyperlink:
                    video = ydl.extract_info(arg, download=False)
                else:
                    video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            except utils.DownloadError as e:
                self.is_appropriate = False
                print(f"logs: {e}")
            
            return video


    def download(self) -> str:
        ydl_opts: dict = {
                            'format': 'bestaudio/best',
                            'outtmpl': self.file_path,
                            'noplaylist':'True',
                            'keepvideo': 'True',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192'
                            }],
                         }

        # Downloads song if it doesn't exist
        if not os.path.exists(self.file_path):
            # Create Downloads folder if not exists
            try:
                os.makedirs(Song.DOWNLOAD_DIR)
            except: pass
            # Keep donwloaded songs under 10
            self.remove_older_files()

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

    
    def hash_title(self) -> str:
        import hashlib
        hash = int(hashlib.sha256(self.title.encode('utf-8')).hexdigest(), 16) % 10**8
        return str(hash)


    @classmethod
    def remove_older_files(cls) -> None:
        try:
            files_in_dir: list = os.listdir(cls.DOWNLOAD_DIR)
            full_path : list= [f"{cls.DOWNLOAD_DIR}/{file}" for file in files_in_dir]

            if len(files_in_dir) >= 100:
                oldest_file = min(full_path, key=os.path.getctime)
                os.remove(oldest_file)
        # Ignores exception when download dir is not yet created
        except FileNotFoundError as e:
            print(e)
