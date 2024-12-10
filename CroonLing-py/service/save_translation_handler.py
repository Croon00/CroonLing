from database.translations_db import TranslationsDB

class SaveTranslationHandler:
    def __init__(self):
        self.translations_db = TranslationsDB()

    def save_translated_lyrics(self, song_id: str, translated_lyrics: str):
        """
        번역된 가사를 데이터베이스에 삽입 또는 업데이트합니다.

        Parameters:
        - song_id: 곡 ID
        - translated_lyrics: 번역된 가사

        Returns:
        - 성공 메시지 (str)
        """
        try:
            # 번역된 가사 업데이트
            self.translations_db.update_translation(song_id, translated_lyrics)
            return f"곡 ID '{song_id}'의 번역된 가사가 성공적으로 업데이트되었습니다."
        except Exception as e:
            print(f"번역된 가사를 업데이트하는 중 오류 발생: {e}")
            return f"곡 ID '{song_id}'의 번역된 가사 업데이트에 실패했습니다."
