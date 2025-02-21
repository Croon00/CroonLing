from database.mongodb import mongo_db

class ArtistsDB:
    def __init__(self):
        self.collection = mongo_db["artists"]

    def find_artist_by_id(self, artist_id):
        """아티스트 ID로 조회"""
        artist = self.collection.find_one({"artist_id": artist_id})
        
        if artist :
            return artist
        else : 
            return None
        

    def find_artist_by_name(self, artist_name):
        """아티스트 이름(영어 또는 한국어)으로 검색 (리스트에서 검색)"""
        artist = self.collection.find_one({"artist_names": artist_name})
        if artist :
            return artist
        else : 
            return None
        
    def upsert_artist(self, artist_id, artist_name):
        """아티스트 정보 삽입 또는 업데이트 (중복 방지 및 오류 해결)"""
        try:
            print(f"[DEBUG] 업서트 실행 - artist_id: {artist_id}, artist_name: {artist_name}")

            # ✅ 기존 아티스트 문서 조회
            existing_artist = self.collection.find_one({"artist_id": artist_id})

            # ✅ 기존 artist_names 필드가 없거나 단일 문자열이면 리스트로 변환
            if existing_artist:
                artist_names = existing_artist.get("artist_names", [])  # 기본값 빈 리스트
                if isinstance(artist_names, str):
                    artist_names = [artist_names]  # 단일 문자열이면 리스트 변환
            else:
                artist_names = []  # 신규 삽입 시 빈 리스트로 초기화

            # ✅ 업데이트 실행
            update_query = {
                "$setOnInsert": {"artist_id": artist_id},  # 처음 삽입될 때만 설정
                "$addToSet": {"artist_names": artist_name}  # 중복되지 않도록 리스트 추가
            }

            print("[DEBUG] 업데이트 실행 준비 완료")

            # ✅ MongoDB에 업데이트 수행 (없으면 삽입)
            result = self.collection.update_one(
                {"artist_id": artist_id},
                update_query,
                upsert=True
            )

            # ✅ 업데이트 결과 출력
            if result.matched_count:
                print(f"[DEBUG] 기존 아티스트 업데이트 완료 - artist_id: {artist_id}")
            elif result.upserted_id:
                print(f"[DEBUG] 신규 아티스트 추가 완료 - artist_id: {artist_id}")
            else:
                print(f"[WARNING] 아티스트 업데이트 없음 - artist_id: {artist_id}")

        except PyMongoError as e:
            print(f"[ERROR] 아티스트 정보 삽입 중 오류 발생: {e}")
            print(f"[DEBUG] 입력 데이터 - artist_id: {artist_id}, artist_name: {artist_name}")

    def insert_artist_name_kr(self, artist_id, korean_name):
        """기존 아티스트에 한국어 이름 추가"""
        existing_artist = self.find_artist_by_id(artist_id)
        if not existing_artist:
            return False  # 아티스트가 DB에 없으면 추가 불가

        self.collection.update_one(
            {"artist_id": artist_id},
            {"$addToSet": {"artist_names": korean_name}},  # 리스트에 추가 (중복 방지)
            upsert=True
        )
        return True
