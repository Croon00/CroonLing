from database.mongodb import mongo_db

class ArtistsDB:
    def __init__(self):
        self.collection = mongo_db["artists"]

    def find_artist_id(self, artist_id):
        """아티스트 조회"""
        return self.collection.find_one({"artist_id": artist_id}) is not None

    def upsert_artist(self, artist_id, artist_name):
        """아티스트 삽입"""
        self.collection.update_one(
            {"artist_id": artist_id},
            {"$set":{"artist_name": artist_name}}, # 없는 경우 삽입
            upsert=True
        )
    
