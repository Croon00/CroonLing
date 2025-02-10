from database import TranslationsDB
from apis import Translator  # 번역 API 가져오기

class TranslationService:
    def __init__(self):
        self.translations_db = TranslationsDB()
        self.translator = Translator()  # Translator 인스턴스를 Service에서 관리

    def get_translated_lyrics(self, song_id):
        """
        번역된 가사 가져오기
        """
        translated_lyrics = self.translations_db.find_translated_lyrics(song_id)
        return translated_lyrics if translated_lyrics else None
    
    def save_translated_lyrics(self, song_id: str, translated_lyrics: str):
        """
        번역된 가사를 데이터베이스에 삽입 또는 업데이트합니다.
        """
        try:
            self.translations_db.upsert_translation(song_id, translated_lyrics)
            return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."
        except Exception as e:
            print(f"번역된 가사를 업데이트하는 중 오류 발생: {e}")
            return f"곡 ID '{song_id}'의 번역된 가사 업데이트에 실패했습니다."

    def translate_lyrics(self, song_id, lyrics):
        """
        가사를 번역하고 DB에 저장
        """
        translation = self.translator.translate(lyrics)  # ✅ 이제 서비스에서 직접 호출
        if not translation or "오류" in translation:
            return None  # 번역 실패 시 None 반환
        
        self.save_translated_lyrics(song_id, translation)  # 번역된 가사 저장
        return translation
