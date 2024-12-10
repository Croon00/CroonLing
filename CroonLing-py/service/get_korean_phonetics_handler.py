from database.translations_db import TranslationsDB


class GetKoreanPhoneticsHandler:
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
