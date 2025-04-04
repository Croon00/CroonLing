from database.mongodb import mongo_db
from pymongo.errors import PyMongoError

class LyricsDB:
    def __init__(self):
        self.collection = mongo_db["lyrics"]

    def upsert_lyrics(self, song_id, lyrics):
        """가사 삽입 또는 업데이트"""
        try:
            self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"lyrics": lyrics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 가사 저장 오류: {e}")

    def upsert_translation(self, song_id, translated_lyrics):
        """번역 가사 삽입 또는 업데이트"""
        try:
            self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"translated_lyrics": translated_lyrics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 번역 가사 저장 오류: {e}")

    def upsert_phonetics(self, song_id, phonetics):
        """로마자 발음 삽입 또는 업데이트"""
        try:
            self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"phonetics_lyrics": phonetics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 발음 저장 오류: {e}")

    def upsert_phonetics_korean(self, song_id, phonetics_korean):
        """한글 발음 삽입 또는 업데이트"""
        try:
            self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"phonetics_korean_lyrics": phonetics_korean}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 한글 발음 저장 오류: {e}")

    def upsert_kanji_info(self, song_id, kanji_info):
        """한자 정보 삽입 또는 업데이트"""
        try:
            self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"kanji_info": kanji_info}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 한자 정보 저장 오류: {e}")

    def find_lyrics_by_id(self, song_id):
        """곡 ID로 lyrics 관련 전체 정보 조회"""
        return self.collection.find_one({"song_id": song_id})  # 모든 필드 포함

    def find_translated_lyrics(self, song_id):
        """번역된 가사만 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"translated_lyrics": 1})
        return song["translated_lyrics"] if song and "translated_lyrics" in song else None

    def find_kanji_info(self, song_id):
        """한자 정보만 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"kanji_info": 1})
        return song["kanji_info"] if song and "kanji_info" in song else None

    def find_phonetics(self, song_id):
        """로마자 발음 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"phonetics_lyrics": 1})
        return song["phonetics_lyrics"] if song and "phonetics_lyrics" in song else None

    def find_phonetics_korean(self, song_id):
        """한글 발음 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"phonetics_korean_lyrics": 1})
        return song["phonetics_korean_lyrics"] if song and "phonetics_korean_lyrics" in song else None
