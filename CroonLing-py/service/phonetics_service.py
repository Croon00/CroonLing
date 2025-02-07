from database.translations_db import TranslationsDB


class PhoneticsService:
    def __init__(self):
        self.db_manager = TranslationsDB()

    def get_phonetics(self, song_id):
        """
        곡의 로마자 발음 가져오기
        """
        phonetics_lyrics = self.db_manager.get_phonetics(song_id)
        if phonetics_lyrics:
            return phonetics_lyrics
        return None



    def save_phonetics(self, song_id: str, phonetics_lyrics: str):
            """
            로마자 발음을 데이터베이스에 삽입 또는 업데이트합니다.

            Parameters:
            - song_id: 곡 ID
            - phonetics_lyrics: 로마자 발음
            Returns:
            - 성공 메시지 (str)
            """
            try:
                # 로마자 발음 업데이트
                self.translations_db.update_phonetics(song_id, phonetics_lyrics)
                return f"곡 ID '{song_id}'의 로마자 발음이 성공적으로 업데이트되었습니다."
            except Exception as e:
                print(f"로마자 발음을 업데이트하는 중 오류 발생: {e}")
                return f"곡 ID '{song_id}'의 로마자 발음 업데이트에 실패했습니다."