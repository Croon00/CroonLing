from database.lyrics_db import LyricsDB


class GetLyricsHandler:
    def __init__(self):
        self.lyrics_db = LyricsDB()

    def get_lyrics(self, song_id):
        """
        특정 곡의 가사를 반환
        :param song_id: 곡 고유 id
        """
        lyrics = self.lyrics_db.get_lyrics(song_id)
        if lyrics:
            return lyrics
        return None
