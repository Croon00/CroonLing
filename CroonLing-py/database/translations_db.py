# from database.mongodb import mongo_db

# class TranslationsDB:
#     def __init__(self):
#         self.collection = mongo_db["translations"]

#     def upsert_translation(self, song_id, translated_lyrics):
#         """번역된 가사 삽입 또는 업데이트"""
#         self.collection.update_one(
#             {"song_id": song_id},
#             {"$set": {"translated_lyrics": translated_lyrics}},
#             upsert=True
#         )

#     def find_translated_lyrics(self, song_id):
#         """번역된 가사 조회"""
#         result = self.collection.find_one({"song_id": song_id})
#         return result["translated_lyrics"] if result else None

