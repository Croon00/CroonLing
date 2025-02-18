from database.mongodb import mongo_db

class ArtistsDB:
    def __init__(self):
        self.collection = mongo_db["artists"]
        self.kr_collection = mongo_db["artist_kr"]  # 한국어 이름 컬렉션

    def find_artist_by_id(self, artist_id):
        """아티스트 ID로 조회"""
        return self.collection.find_one({"artist_id": artist_id})

    def find_artist_by_name(self, artist_name):
        """아티스트 이름(영어 또는 한국어)으로 검색"""
        artist = self.collection.find_one({"artist_name": artist_name})
        if not artist:
            artist_kr = self.kr_collection.find_one({"korean_name": artist_name})
            if artist_kr:
                artist = self.collection.find_one({"artist_id": artist_kr["artist_id"]})
        return artist

    def upsert_artist(self, artist_id, artist_name):
        """아티스트 정보 저장 (Spotify에서 검색 후 저장하는 로직 그대로 유지)"""
        self.collection.update_one(
            {"artist_id": artist_id},
            {"$set": {"artist_name": artist_name}},  # 영어 이름 저장 (기존 유지)
            upsert=True
        )

    def insert_artist_name_kr(self, artist_id, korean_name):
        """기존 아티스트에 한국어 이름 추가"""
        existing_artist = self.find_artist_by_id(artist_id)
        if not existing_artist:
            return False  # 아티스트가 DB에 없으면 추가 불가

        self.kr_collection.update_one(
            {"artist_id": artist_id},
            {"$set": {"korean_name": korean_name}},
            upsert=True
        )
        return True
