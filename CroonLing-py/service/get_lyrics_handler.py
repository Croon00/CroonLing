from database.lyrics_db import LyricsDB


class GetLyricsHandler:
    def __init__(self):
        self.lyrics_db = LyricsDB()

    def get_lyrics(self, artist_name, song_name):
        """
        특정 곡의 저장된 가사 조회
        :param artist_name: 가수 이름
        :param song_name: 곡 제목
        :return: 저장된 가사 또는 '저장되지 않은 곡입니다.'
        """
        lyrics = self.lyrics_db.get_lyrics(artist_name, song_name)
        if lyrics:
            return lyrics
        return "저장되지 않은 곡입니다."
