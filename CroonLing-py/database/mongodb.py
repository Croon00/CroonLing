from pymongo import MongoClient
import os

# MongoDB 연결 설정
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
mongo_db = client["croonling_db"]  # 데이터베이스 이름 설정
