from database.mongodb import mongo_db

class TranslationsDB:
    def __init__(self):
        self.collection = mongo_db["translations"]

    def update_translation(self, song_id, translated_lyrics):
        """번역된 가사 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"translated_lyrics": translated_lyrics}},
            upsert=True
        )

    def get_translated_lyrics(self, song_id):
        """번역된 가사 조회"""
        result = self.collection.find_one({"song_id": song_id})
        return result["translated_lyrics"] if result else None

    def update_phonetics(self, song_id, phonetics_lyrics):
        """로마자 발음 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"phonetics_lyrics": phonetics_lyrics}},
            upsert=True
        )

    def get_phonetics(self, song_id):
        """로마자 발음 조회"""
        result = self.collection.find_one({"song_id": song_id})
        return result["phonetics_lyrics"] if result else None

    def update_korean_phonetics(self, song_id, korean_phonetics_lyrics):
        """한국어 발음 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"korean_phonetics_lyrics": korean_phonetics_lyrics}},
            upsert=True
        )

    def get_korean_phonetics(self, song_id):
        """한국어 발음 조회"""
        result = self.collection.find_one({"song_id": song_id})
        return result["korean_phonetics_lyrics"] if result else None
