from collections import deque

class SongQueue:
    def __init__(self) -> None:
        self.queue = deque([])
        self.current = None

    def add_song(self, song) -> None:
        # print(f'Added {song.title} to queue.')
        if self.current == None:
            self.current = song
        self.queue.appendleft(song)
    
    def get_next_song(self) -> str or None:
        try:
            self.current = self.queue.pop()
            return self.current
        except IndexError:
            return None
