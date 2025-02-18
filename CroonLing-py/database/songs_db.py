from database.mongodb import mongo_db

class SongsDB:
    def __init__(self):
        self.collection = mongo_db["songs"]

    def upsert_song(self, track):
        """곡 정보 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": track["song_id"]},  # song_id 기준으로 찾음
            {
                "$set": {
                    "artist_id": track["artist_id"],
                    "artist_name": track["artist_name"],
                    "song_name": track["song_name"],
                    "album_name": track.get("album_name"),
                    "release_date": track.get("release_date"),
                    "track_image_url": track.get("track_image_url"),
                    "url": track.get("url"),
                    "$setOnInsert": {  # 초기 삽입 시만 설정
                        "korean_song_names": [],
                        "lyrics": None,
                        "translated_lyrics": None,
                        "phonetics_lyrics": None,
                        "phonetics_korean_lyrics": None
                    }
                }
            },
            upsert=True  # 없으면 삽입
        )

    def upsert_lyrics(self, song_id, lyrics):
        """가사 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"lyrics": lyrics}},
            upsert=True
        )

    def upsert_translation(self, song_id, translated_lyrics):
        """번역된 가사 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"translated_lyrics": translated_lyrics}},
            upsert=True
        )

    def upsert_phonetics(self, song_id, phonetics):
        """발음 데이터 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"phonetics_lyrics": phonetics}},
            upsert=True
        )

    def upsert_phonetics_korean(self, song_id, phonetics_korean):
        """한국어 발음 데이터 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"phonetics_korean_lyrics": phonetics_korean}},
            upsert=True
        )

    def insert_song_name_kr(self, song_id, korean_name):
        """곡에 한국어 이름 추가"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$addToSet": {"korean_song_names": korean_name}},  # 리스트에 추가 (중복 방지)
            upsert=True
        )

    def find_song_by_id(self, song_id):
        """곡 ID로 곡 정보 조회"""
        return self.collection.find_one({"song_id": song_id})

    def find_song_by_artist(self, artist_id, song_name):
        """아티스트 ID와 곡명으로 곡 정보 조회"""
        return self.collection.find_one({"artist_id": artist_id, "song_name": song_name})

    def find_translated_lyrics(self, song_id):
        """번역된 가사 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"translated_lyrics": 1})
        return song["translated_lyrics"] if song and "translated_lyrics" in song else None
