from database.lyrics_db import LyricsDB


class GetLyricsHandler:
    def __init__(self):
        self.lyrics_db = LyricsDB()

    def get_lyrics(self, artist_name, song_name):
        """
        특정 곡의 가사를 반환
        :param artist_name: 가수 이름
        :param song_name: 곡 제목
        :return: 곡의 lyrics (가사 문자열) 또는 None
        """
        return self.lyrics_db.get_lyrics(artist_name, song_name)
