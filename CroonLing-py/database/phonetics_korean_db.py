# from database.mongodb import mongo_db

# class PhoneticsKoreanDB:
#     def __init__(self):
#         self.collection = mongo_db["phonetics_korean"]

#     def find_phonetics_korean(self, song_id):
#         """한국 발음 조회"""
#         return self.collection.find_one({"song_id": song_id}) is not None

#     def upsert_phonetics_korean(self, song_id, phonetics_korean):
#         """한국어 발음 삽입 또는 업데이트 (최적화된 방식)"""
#         self.collection.update_one(
#             {"song_id": song_id},  # song_id가 같은 문서 찾기
#             {"$set": {"phonetics_korean": phonetics_korean}},  # 값이 있으면 업데이트
#             upsert=True  # 없으면 삽입
#         )    
