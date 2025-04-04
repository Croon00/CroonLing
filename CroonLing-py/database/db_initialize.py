from database.mongodb import mongo_db

def initialize_mongodb():
    """MongoDB 컬렉션 초기화 및 기본 인덱스 설정"""

    # ✅ 아티스트 컬렉션 (여러 이름을 저장)
    artists_collection = mongo_db["artists"]
    artists_collection.create_index("artist_id", unique=True)
    artists_collection.create_index("artist_names")  # 다국어 이름 검색 최적화

    # ✅ 곡 컬렉션 (곡 메타 정보만 포함)
    songs_collection = mongo_db["songs"]
    songs_collection.create_index("song_id", unique=True)
    songs_collection.create_index("artist_id")
    songs_collection.create_index("song_names")
    songs_collection.create_index("artist_names")

    # ✅ 가사 컬렉션 (가사, 번역, 발음, 한자 등)
    lyrics_collection = mongo_db["lyrics"]
    lyrics_collection.create_index("song_id", unique=True)  # 1:1 매핑을 위해 고유 인덱스

    print("✅ MongoDB 데이터베이스 초기화 완료!")

if __name__ == "__main__":
    initialize_mongodb()
