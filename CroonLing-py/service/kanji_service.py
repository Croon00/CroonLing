from database import LyricsDB  # ✅ 변경된 DB 클래스 사용
from apis import ChatgptApi
import logging

class KanjiService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.translator = ChatgptApi()
        self.logger = logging.getLogger(__name__)

    async def get_kanji_info(self, song_id):
        kanji_info = await self.lyrics_db.find_kanji_info(song_id)
        if kanji_info:
            self.logger.info(f"✅ 한자 정보 조회 성공 (ID: {song_id})")
            return kanji_info

        self.logger.warning(f"⚠️ 한자 정보 없음 (ID: {song_id})")
        return None

    async def save_kanji_info(self, song_id, kanji_info):
        self.logger.info(f"📜 한자 정보 저장: 곡 ID '{song_id}'")
        await self.lyrics_db.upsert_kanji_info(song_id, kanji_info)
        return f"곡 ID '{song_id}'의 한자 정보가 성공적으로 저장되었습니다."

    async def lyrics_to_kanji(self, song_id, lyrics):
        kanji_info = await self.translator.extract_kanji_info(lyrics)
        if kanji_info:
            await self.save_kanji_info(song_id, kanji_info)
            return kanji_info
        return None
