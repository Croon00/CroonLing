from database.mongodb import mongo_db

class SongsDB:
    def __init__(self):
        self.collection = mongo_db["songs"]

    def insert_song(self, track):
        """곡 정보를 삽입"""
        if not self.get_song_info(track["artist_id"], track["song_name"]):
            self.collection.insert_one({
                "song_id": track["song_id"],
                "artist_id": track["artist_id"],
                "song_name": track["song_name"],
                "release_date": track.get("release_date"),
                "track_image_url": track.get("track_image_url"),
                "album_name": track.get("album_name"),
            })


    def get_song_info(self, artist_name, song_name):
        """곡 정보 조회"""
        return self.collection.find_one({"artist_name": artist_name, "song_name": song_name})
