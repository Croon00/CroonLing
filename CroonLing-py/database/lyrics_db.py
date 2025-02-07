from database.mongodb import mongo_db

class LyricsDB:
    def __init__(self):
        self.collection = mongo_db["lyrics"]

    def find_lyrics_id(self, song_id):
        """곡 가사 저장 여부 확인"""
        return self.collection.find_one({"song_id": song_id}) is not None

    def upsert_lyrics(self, song_id, lyrics):
        self.collection.update_one(
            {"song_id": song_id},
            {"$set":{"lyrics": lyrics}},
            upsert=True
        )
