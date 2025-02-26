from database.songs_db import SongsDB
from apis import ChatgptApi
import logging

class KanjiService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.translator = ChatgptApi()
        self.logger = logging.getLogger(__name__)
        
    def get_kanji_info(self, song_id):
        """한자 정보 가져오기"""
        song = self.songs_db.find_kanji_info(song_id)
        if song:
            self.logger.info(f"✅ 한자 정보 조회 성공 (ID: {song_id})")
            return song.get("kanji_info")
        self.logger.warning(f"⚠️ 한자 정보 없음 (ID: {song_id})")
        return None
    
    
    def save_kanji_info(self, song_id, kanji_info):
        """한자 정보 저장"""
        self.logger.info(f"📜 한자 정보 저장: 곡 ID '{song_id}'")
        self.songs_db.upsert_kanji_info(song_id, kanji_info)
        return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."

    def lyrics_to_kanji(self, song_id, lyrics):
        """가사로 부터 한자 정보 얻기"""
        kanji_info = self.translator.extract_kanji_info(lyrics)
        if kanji_info:
            self.save_kanji_info(song_id, kanji_info)
            return kanji_info
        return None
    
