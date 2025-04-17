from database.lyrics_db import LyricsDB  # ✅ 변경된 DB 클래스
from apis import ChatgptApi

class TranslationService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.translator = ChatgptApi()

    async def get_translated_lyrics(self, song_id):
        return await self.lyrics_db.find_translated_lyrics(song_id)

    async def save_translated_lyrics(self, song_id, translated_lyrics):
        await self.lyrics_db.upsert_translation(song_id, translated_lyrics)
        return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."

    async def translate_lyrics(self, song_id, lyrics):
        translation = await self.translator.translate(lyrics)
        if translation:
            await self.save_translated_lyrics(song_id, translation)
            return translation
        return None
