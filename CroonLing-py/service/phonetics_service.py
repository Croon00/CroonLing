from database.lyrics_db import LyricsDB  # ✅ 직접 참조
from apis import ChatgptApi

class PhoneticsService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.translator = ChatgptApi()

    async def get_phonetics(self, song_id):
        return await self.lyrics_db.find_phonetics(song_id)

    async def generate_and_save_phonetics(self, song_id):
        song_data = await self.lyrics_db.find_lyrics_by_id(song_id)
        lyrics = song_data.get("lyrics") if song_data else None
        if not lyrics:
            return None

        pronunciation = await self.translator.phonetics(lyrics)
        if pronunciation:
            await self.lyrics_db.upsert_phonetics(song_id, pronunciation)
            return pronunciation

        return None
