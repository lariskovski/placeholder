from collections import deque


class SongQueue:
    def __init__(self) -> None:
        self.queue = deque([])

    def add_song(self, song) -> None:
        print(f'Added {song} to queue.')
        self.queue.appendleft(song)
    
    def get_next_song(self) -> str or None:
        try:
            return self.queue.pop()
        except IndexError:
            return None

if __name__ == "__main__":
    queu = SongQueue()

    queu.add_song('i gotta feeling')

    print(queu.get_next_song())
    print(queu.get_next_song())