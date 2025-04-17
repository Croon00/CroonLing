from database.mongodb import mongo_db
from pymongo.errors import PyMongoError

class ArtistsDB:
    def __init__(self):
        self.collection = mongo_db["artists"]

    async def find_artist_by_id(self, artist_id):
        artist = await self.collection.find_one({"artist_id": artist_id})
        return artist if artist else None

    async def find_artist_by_name(self, artist_name):
        artist = await self.collection.find_one({"artist_names": artist_name})
        return artist if artist else None

    async def upsert_artist(self, artist_info):
        try:
            artist_id = artist_info["artist_id"]
            artist_name = artist_info["artist_name"]

            existing_artist = await self.collection.find_one({"artist_id": artist_id})

            artist_names = []
            if existing_artist:
                artist_names = existing_artist.get("artist_names", [])
                if isinstance(artist_names, str):
                    artist_names = [artist_names]

            update_query = {
                "$set": {
                    "followers": artist_info["followers"],
                    "genres": artist_info["genres"],
                    "images": artist_info["images"],
                    "popularity": artist_info["popularity"]
                },
                "$addToSet": {"artist_names": artist_name}
            }

            await self.collection.update_one(
                {"artist_id": artist_id},
                update_query,
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 아티스트 정보 삽입 중 오류 발생: {e}")

    async def insert_artist_name_kr(self, artist_id, korean_name):
        existing_artist = await self.find_artist_by_id(artist_id)
        if not existing_artist:
            return False

        await self.collection.update_one(
            {"artist_id": artist_id},
            {"$addToSet": {"artist_names": korean_name}},
            upsert=True
        )
        return True
