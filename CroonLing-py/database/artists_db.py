from database.mongodb import mongo_db

class ArtistsDB:
    def __init__(self):
        self.collection = mongo_db["artists"]

    def get_artist(self, artist_id):
        """아티스트 저장 여부 확인"""
        return self.collection.find_one({"artist_id": artist_id}) is not None

    def insert_artist_name(self, artist_id, artist_name):
        """아티스트 이름 삽입"""
        if not self.get_artist(artist_id):
            self.collection.insert_one({"artist_id": artist_id, "artist_name": artist_name})
