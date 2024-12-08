from database.db_manager import DBManager


class KoreanPhoneticsHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def get_korean_phonetics(self, artist, song):
        """
        곡의 한글 발음 가져오기
        """
        korean_phonetics = self.db_manager.get_korean_phonetics(artist, song)
        if korean_phonetics:
            return korean_phonetics
        return "저장되지 않은 곡입니다."
