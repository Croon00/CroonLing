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
                    "song_name": track["song_name"],
                    "release_date": track.get("release_date"),
                    "track_image_url": track.get("track_image_url"),
                    "album_name": track.get("album_name"),
                }
            },
            upsert=True  # 없으면 삽입
        )

    def find_song_by_id(self, song_id):
        """곡 ID로 곡 정보 조회"""
        return self.collection.find_one({"song_id": song_id})

    def find_song_by_artist(self, artist_id, song_name):
        """아티스트 ID와 곡명으로 곡 정보 조회"""
        return self.collection.find_one({"artist_id": artist_id, "song_name": song_name})
