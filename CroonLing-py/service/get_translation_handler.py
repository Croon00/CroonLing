from database.translations_db import TranslationsDB


class GetTranslationHandler:
    def __init__(self):
        self.db_manager = TranslationsDB()

    def get_translated_lyrics(self, song_id):
        """
        번역된 가사 가져오기
        """
        translated_lyrics = self.db_manager.get_translated_lyrics(song_id)
        if translated_lyrics:
            return translated_lyrics
        return None
