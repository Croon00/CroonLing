from pymongo import MongoClient
import os

# MongoDB 연결 설정
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
mongo_db = client["croonling_db"]  # 데이터베이스 이름 설정

def initialize_mongodb():
    """MongoDB 컬렉션 초기화 및 기본 인덱스 설정"""
    
    # 아티스트 컬렉션 생성
    artists_collection = mongo_db["artists"]
    artists_collection.create_index("artist_id", unique=True)  # 아티스트 ID를 유니크 키로 설정

    # 곡 컬렉션 생성
    songs_collection = mongo_db["songs"]
    songs_collection.create_index("song_id", unique=True)  # 곡 ID를 유니크 키로 설정
    songs_collection.create_index("artist_id")  # 아티스트 ID로 조회 가능하게 인덱스 설정

    # 한국어 아티스트 이름 컬렉션 생성
    artist_kr_collection = mongo_db["artist_kr"]
    artist_kr_collection.create_index("artist_id")  # 아티스트 ID 기준 인덱스 설정

    # 가사 컬렉션 생성
    lyrics_collection = mongo_db["lyrics"]
    lyrics_collection.create_index("song_id", unique=True)  # 곡 ID를 유니크 키로 설정

    # 번역된 가사 컬렉션 생성
    translations_collection = mongo_db["translations"]
    translations_collection.create_index("song_id", unique=True)

    # 발음 데이터 컬렉션 생성
    phonetics_collection = mongo_db["phonetics"]
    phonetics_collection.create_index("song_id", unique=True)

    print("✅ MongoDB 데이터베이스 초기화 완료!")

if __name__ == "__main__":
    initialize_mongodb()
