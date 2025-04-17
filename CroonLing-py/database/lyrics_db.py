from database.mongodb import mongo_db
from pymongo.errors import PyMongoError

class LyricsDB:
    def __init__(self):
        self.collection = mongo_db["lyrics"]

    async def upsert_lyrics(self, song_id, lyrics):
        try:
            await self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"lyrics": lyrics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 가사 저장 오류: {e}")

    async def upsert_translation(self, song_id, translated_lyrics):
        try:
            await self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"translated_lyrics": translated_lyrics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 번역 가사 저장 오류: {e}")

    async def upsert_phonetics(self, song_id, phonetics):
        try:
            await self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"phonetics_lyrics": phonetics}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 발음 저장 오류: {e}")

    async def upsert_phonetics_korean(self, song_id, phonetics_korean):
        try:
            await self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"phonetics_korean_lyrics": phonetics_korean}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 한글 발음 저장 오류: {e}")

    async def upsert_kanji_info(self, song_id, kanji_info):
        try:
            await self.collection.update_one(
                {"song_id": song_id},
                {"$set": {"kanji_info": kanji_info}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"[ERROR] 한자 정보 저장 오류: {e}")

    async def find_lyrics_by_id(self, song_id):
        return await self.collection.find_one({"song_id": song_id})

    async def find_translated_lyrics(self, song_id):
        song = await self.collection.find_one({"song_id": song_id}, {"translated_lyrics": 1})
        return song.get("translated_lyrics") if song else None

    async def find_kanji_info(self, song_id):
        song = await self.collection.find_one({"song_id": song_id}, {"kanji_info": 1})
        return song.get("kanji_info") if song else None

    async def find_phonetics(self, song_id):
        song = await self.collection.find_one({"song_id": song_id}, {"phonetics_lyrics": 1})
        return song.get("phonetics_lyrics") if song else None

    async def find_phonetics_korean(self, song_id):
        song = await self.collection.find_one({"song_id": song_id}, {"phonetics_korean_lyrics": 1})
        return song.get("phonetics_korean_lyrics") if song else None
