from database.lyrics_db import LyricsDB  # ✅ 변경된 DB 클래스
from apis import ChatgptApi

class TranslationService:
    def __init__(self):
        self.lyrics_db = LyricsDB()  # ✅ SongsDB → LyricsDB
        self.translator = ChatgptApi()

    def get_translated_lyrics(self, song_id):
        """번역된 가사 가져오기"""
        return self.lyrics_db.find_translated_lyrics(song_id)

    def save_translated_lyrics(self, song_id, translated_lyrics):
        """번역된 가사를 저장"""
        self.lyrics_db.upsert_translation(song_id, translated_lyrics)
        return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."

    def translate_lyrics(self, song_id, lyrics):
        """가사를 번역하고 저장"""
        translation = self.translator.translate(lyrics)
        if translation:
            self.save_translated_lyrics(song_id, translation)
            return translation
        return None
