from database.mongodb import mongo_db

def initialize_mongodb():
    """MongoDB 컬렉션 초기화 및 기본 인덱스 설정"""

    # ✅ 아티스트 컬렉션
    artists_collection = mongo_db["artists"]
    artists_collection.create_index("artist_id", unique=True)

    # ✅ 곡 컬렉션
    songs_collection = mongo_db["songs"]
    songs_collection.create_index("song_id", unique=True)
    songs_collection.create_index("artist_id")

    # ✅ 한국어 아티스트 이름 컬렉션
    artist_kr_collection = mongo_db["artist_kr"]
    artist_kr_collection.create_index("artist_id")

    # ✅ 가사 컬렉션
    lyrics_collection = mongo_db["lyrics"]
    lyrics_collection.create_index("song_id", unique=True)

    # ✅ 번역된 가사 컬렉션
    translations_collection = mongo_db["translations"]
    translations_collection.create_index("song_id", unique=True)

    # ✅ 발음 데이터 컬렉션 (로마자 발음)
    phonetics_collection = mongo_db["phonetics"]
    phonetics_collection.create_index("song_id", unique=True)

    # ✅ 한국어 발음 데이터 컬렉션 (누락된 부분 추가)
    phonetics_korean_collection = mongo_db["phonetics_korean"]
    phonetics_korean_collection.create_index("song_id", unique=True)  # 곡 ID 기준 인덱스 설정

    print("✅ MongoDB 데이터베이스 초기화 완료! (한국어 발음 컬렉션 추가됨)")

if __name__ == "__main__":
    initialize_mongodb()
