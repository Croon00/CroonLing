# from database.mongodb import mongo_db

# class PhoneticsDB:
#     def __init__(self):
#         self.collection = mongo_db["phonetics"]

#     def find_phonetics(self, song_id):
#         """아티스트 저장 여부 확인"""
#         return self.collection.find_one({"song_id": song_id}) is not None

#     def upsert_phonetics(self, song_id, phonetics):
#         """아티스트 삽입 또는 업데이트"""
#         self.collection.update_one(
#             {"song_id": song_id},
#             {"$set": {"phonetics":phonetics}},
#             upsert=True
#         )