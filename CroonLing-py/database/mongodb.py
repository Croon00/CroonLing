from pymongo import MongoClient
from config_loader import load_config

# ✅ MongoDB Atlas 연결
config = load_config()
client = MongoClient(config.get('MONGO_URI'))
mongo_db = client["croonling_db"]

print("✅ MongoDB Atlas 연결 성공!")
