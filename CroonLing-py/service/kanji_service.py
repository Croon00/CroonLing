from database.lyrics_db import LyricsDB  # ✅ 변경된 DB 클래스 사용
from apis import ChatgptApi
import logging

class KanjiService:
    def __init__(self):
        self.lyrics_db = LyricsDB()  # ✅ Lyrics 컬렉션 전용 DB
        self.translator = ChatgptApi()
        self.logger = logging.getLogger(__name__)

    def get_kanji_info(self, song_id):
        """한자 정보 가져오기"""
        kanji_info = self.lyrics_db.find_kanji_info(song_id)
        if kanji_info:
            self.logger.info(f"✅ 한자 정보 조회 성공 (ID: {song_id})")
            return kanji_info

        self.logger.warning(f"⚠️ 한자 정보 없음 (ID: {song_id})")
        return None

    def save_kanji_info(self, song_id, kanji_info):
        """한자 정보 저장"""
        self.logger.info(f"📜 한자 정보 저장: 곡 ID '{song_id}'")
        self.lyrics_db.upsert_kanji_info(song_id, kanji_info)
        return f"곡 ID '{song_id}'의 한자 정보가 성공적으로 저장되었습니다."

    def lyrics_to_kanji(self, song_id, lyrics):
        """가사로부터 한자 정보 추출"""
        kanji_info = self.translator.extract_kanji_info(lyrics)
        if kanji_info:
            self.save_kanji_info(song_id, kanji_info)
            return kanji_info
        return None
