from database.translations_db import TranslationsDB


class PhoneticsKoreanService:
    def __init__(self):
        self.translations_db = TranslationsDB()

    def get_korean_phonetics(self, song_id):
        """
        곡의 한글 발음 가져오기
        """
        korean_phonetics = self.translations_db.get_korean_phonetics(song_id)
        if korean_phonetics:
            return korean_phonetics
        return None

    def save_korean_phonetics(self, song_id: str, korean_phonetics_lyrics: str):
            """
            한국어 발음을 데이터베이스에 삽입 또는 업데이트합니다.

            Parameters:
            - song_id: 곡 ID
            - korean_phonetics_lyrics: 한국어 발음
            Returns:
            - 성공 메시지 (str)
            """
            try:
                # 한국어 발음 업데이트
                self.translations_db.update_korean_phonetics(song_id, korean_phonetics_lyrics)
                return f"곡 ID '{song_id}'의 한국어 발음이 성공적으로 업데이트되었습니다."
            except Exception as e:
                print(f"한국어 발음을 업데이트하는 중 오류 발생: {e}")
                return f"곡 ID '{song_id}'의 한국어 발음 업데이트에 실패했습니다."
