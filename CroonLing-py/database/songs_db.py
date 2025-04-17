from database.mongodb import mongo_db
from pymongo.errors import PyMongoError

class SongsDB:
    def __init__(self):
        self.collection = mongo_db["songs"]

    async def upsert_song(self, track):
        try:
            existing_song = await self.collection.find_one({"song_id": track["song_id"]})

            song_names = existing_song.get("song_names", []) if existing_song else []
            artist_names = existing_song.get("artist_names", []) if existing_song else []

            if isinstance(song_names, str):
                song_names = [song_names]
            if isinstance(artist_names, str):
                artist_names = [artist_names]

            new_song_name = track["song_name"]
            new_artist_name = track["artist_name"]

            if new_song_name not in song_names:
                song_names.append(new_song_name)
            if new_artist_name not in artist_names:
                artist_names.append(new_artist_name)

            update_query = {
                "$set": {
                    "artist_id": track["artist_id"],
                    "artist_names": artist_names,
                    "song_names": song_names,
                    "album_name": track.get("album_name"),
                    "release_date": track.get("release_date"),
                    "track_image_url": track.get("track_image_url"),
                    "url": track.get("url")
                }
            }

            result = await self.collection.update_one(
                {"song_id": track["song_id"]},
                update_query,
                upsert=True
            )

            if result.matched_count > 0:
                print(f"[DEBUG] 기존 곡 정보 업데이트 완료 - song_id: {track['song_id']}")
            elif result.upserted_id:
                print(f"[DEBUG] 신규 곡 추가 완료 - song_id: {track['song_id']}")
            else:
                print(f"[WARNING] 곡 정보 업데이트 없음 - song_id: {track['song_id']}")

        except PyMongoError as e:
            print(f"[ERROR] 곡 정보 삽입 중 오류 발생: {e}")
        except Exception as e:
            print(f"[ERROR] 예상치 못한 오류 발생: {e}")

    async def insert_song_name(self, song_id, song_name):
        await self.collection.update_one(
            {"song_id": song_id},
            {"$addToSet": {"song_names": song_name}},
            upsert=True
        )

    async def find_song_by_id(self, song_id):
        return await self.collection.find_one({"song_id": song_id})

    async def find_song_by_artist_id(self, artist_id, song_name):
        song = await self.collection.find_one({"artist_id": artist_id, "song_names": song_name})
        return song if song else None

    async def find_song_by_artist_name(self, artist_name, song_name):
        song = await self.collection.find_one({
            "artist_names": artist_name,
            "song_names": song_name
        })
        return song if song else None
