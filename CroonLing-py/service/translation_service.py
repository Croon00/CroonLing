from database.songs_db import SongsDB
from apis import Translator

class TranslationService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.translator = Translator()

    def get_translated_lyrics(self, song_id):
        """번역된 가사 가져오기"""
        song = self.songs_db.find_song_by_id(song_id)
        return song.get("translated_lyrics") if song else None

    def save_translated_lyrics(self, song_id, translated_lyrics):
        """번역된 가사를 저장"""
        self.songs_db.upsert_translation(song_id, translated_lyrics)
        return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."

    def translate_lyrics(self, song_id, lyrics):
        """가사를 번역하고 저장"""
        print("가사 번역 service 시작")
        print(lyrics)
        translation = self.translator.translate(lyrics)
        print("가사 번역 시작 서비스 후")
        if translation:
            self.save_translated_lyrics(song_id, translation)
            return translation
        return None
    
