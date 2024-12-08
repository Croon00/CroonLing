from database.db_manager import DBManager


class PhoneticsHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def get_phonetics(self, artist, song):
        """
        곡의 로마자 발음 가져오기
        """
        phonetics_lyrics = self.db_manager.get_phonetics(artist, song)
        if phonetics_lyrics:
            return phonetics_lyrics
        return "저장되지 않은 곡입니다."
