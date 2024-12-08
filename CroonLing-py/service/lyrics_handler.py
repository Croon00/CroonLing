from database.db_manager import DBManager


class LyricsHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def get_lyrics(self, artist, song):
        """
        특정 곡의 저장된 가사 조회
        """
        lyrics = self.db_manager.get_lyrics(artist, song)
        if lyrics:
            return lyrics
        return "저장되지 않은 곡입니다."
