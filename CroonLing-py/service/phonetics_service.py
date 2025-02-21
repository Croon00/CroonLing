from database.songs_db import SongsDB
from apis import ChatgptApi
from service.lyrics_service import LyricsService

class PhoneticsService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.translator = ChatgptApi()
        self.lyrics_service = LyricsService()

    def get_phonetics(self, song_id):
        """곡의 로마자 발음 가져오기"""
        song = self.songs_db.find_song_by_id(song_id)
        return song.get("phonetics_lyrics") if song else None

    def generate_and_save_phonetics(self, song_id):
        """곡의 가사에서 발음을 생성하고 DB에 저장"""
        lyrics = self.lyrics_service.get_lyrics(song_id)
        if not lyrics:
            return None

        pronunciation = self.translator.phonetics(lyrics)
        if pronunciation:
            self.songs_db.upsert_phonetics(song_id, pronunciation)
            return pronunciation

        return None
