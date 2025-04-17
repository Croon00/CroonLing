from database.lyrics_db import LyricsDB  # ✅ Lyrics 전용 DB 사용
from service.phonetics_service import PhoneticsService
from apis import ChatgptApi

class PhoneticsKoreanService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.phonetics_service = PhoneticsService()
        self.translator = ChatgptApi()

    async def get_korean_phonetics(self, song_id):
        return await self.lyrics_db.find_phonetics_korean(song_id)

    async def generate_and_save_korean_phonetics(self, song_id):
        roman_pronunciation = await self.phonetics_service.get_phonetics(song_id)
        if not roman_pronunciation:
            return None

        korean_pronunciation = await self.translator.roman_to_korean(roman_pronunciation)
        if korean_pronunciation:
            await self.lyrics_db.upsert_phonetics_korean(song_id, korean_pronunciation)
            return korean_pronunciation

        return None
