from database.songs_db import SongsDB
from service.phonetics_service import PhoneticsService
from apis import Translator

class PhoneticsKoreanService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.phonetics_service = PhoneticsService()
        self.translator = Translator()

    def get_korean_phonetics(self, song_id):
        """곡의 한글 발음 가져오기"""
        song = self.songs_db.find_song_by_id(song_id)
        return song.get("phonetics_korean_lyrics") if song else None

    def generate_and_save_korean_phonetics(self, song_id):
        """로마자 발음을 기반으로 한글 발음을 생성하고 저장"""
        roman_pronunciation = self.phonetics_service.get_phonetics(song_id)
        if not roman_pronunciation:
            return None

        korean_pronunciation = self.translator.roman_to_korean(roman_pronunciation)
        if korean_pronunciation:
            self.songs_db.upsert_phonetics_korean(song_id, korean_pronunciation)
            return korean_pronunciation

        return None
