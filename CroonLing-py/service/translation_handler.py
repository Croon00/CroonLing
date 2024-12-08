from database.db_manager import DBManager


class TranslationHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def get_translated_lyrics(self, artist, song):
        """
        번역된 가사 가져오기
        """
        translated_lyrics = self.db_manager.get_translated_lyrics(artist, song)
        if translated_lyrics:
            return translated_lyrics
        return "저장되지 않은 곡입니다."
