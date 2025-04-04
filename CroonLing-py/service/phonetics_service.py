from database.lyrics_db import LyricsDB  # ✅ 직접 참조
from apis import ChatgptApi

class PhoneticsService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.translator = ChatgptApi()

    def get_phonetics(self, song_id):
        """곡의 로마자 발음 가져오기"""
        return self.lyrics_db.find_phonetics(song_id)

    def generate_and_save_phonetics(self, song_id):
        """곡의 가사에서 발음을 생성하고 DB에 저장"""
        lyrics = self.lyrics_db.find_lyrics_by_id(song_id).get("lyrics") 
        if not lyrics:
            return None

        pronunciation = self.translator.phonetics(lyrics)
        if pronunciation:
            self.lyrics_db.upsert_phonetics(song_id, pronunciation)
            return pronunciation

        return None
