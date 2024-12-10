from database.translations_db import TranslationsDB


class GetPhoneticsHandler:
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
