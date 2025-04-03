from database.mongodb import mongo_db

class SongsDB:
    def __init__(self):
        self.collection = mongo_db["songs"]

    from pymongo.errors import PyMongoError

    def upsert_song(self, track):
        """곡 정보 삽입 또는 업데이트 (여러 이름 저장)"""
        try:

            # ✅ 기존 곡 데이터 조회
            existing_song = self.collection.find_one({"song_id": track["song_id"]})

            # ✅ 기존 song_names 및 artist_names 필드가 없거나 문자열이면 리스트로 변환
            song_names = existing_song.get("song_names", []) if existing_song else []
            artist_names = existing_song.get("artist_names", []) if existing_song else []

            if isinstance(song_names, str):
                song_names = [song_names]  # 단일 문자열이면 리스트 변환
            if isinstance(artist_names, str):
                artist_names = [artist_names]  # 단일 문자열이면 리스트 변환

            # ✅ 현재 track의 `song_name`과 `artist_name`을 리스트에 추가 (중복 방지)
            new_song_name = track["song_name"]
            new_artist_name = track["artist_name"]

            if new_song_name not in song_names:
                song_names.append(new_song_name)
            if new_artist_name not in artist_names:
                artist_names.append(new_artist_name)


            # ✅ MongoDB 업데이트 쿼리 준비
            update_query = {
                "$set": {
                    "artist_id": track["artist_id"],  # ✅ 아티스트 ID만 저장 (정규화)
                    "artist_names": artist_names,  # ✅ 가수 이름 리스트 업데이트
                    "song_names": song_names,  # ✅ 곡 이름 리스트 업데이트
                    "album_name": track.get("album_name"),
                    "release_date": track.get("release_date"),
                    "track_image_url": track.get("track_image_url"),
                    "url": track.get("url")
                }
            }

            # ✅ 처음 삽입되는 경우 `lyrics` 등의 필드 초기화
            if not existing_song:
                update_query["$setOnInsert"] = {
                    "lyrics": None,
                    "translated_lyrics": None,
                    "phonetics_lyrics": None,
                    "phonetics_korean_lyrics": None
                }

            
            # ✅ MongoDB에 업데이트 수행 (없으면 삽입)
            result = self.collection.update_one(
                {"song_id": track["song_id"]},
                update_query,
                upsert=True
            )


            # ✅ 업데이트 결과 출력
            if result.matched_count > 0:
                print(f"[DEBUG] 기존 곡 정보 업데이트 완료 - song_id: {track['song_id']}")
            elif result.upserted_id:
                print(f"[DEBUG] 신규 곡 추가 완료 - song_id: {track['song_id']}")
            else:
                print(f"[WARNING] 곡 정보 업데이트 없음 - song_id: {track['song_id']}")

        except PyMongoError as e:
            print(f"[ERROR] 곡 정보 삽입 중 오류 발생: {e}")
            print(f"[DEBUG] 입력 데이터 - song_id: {track['song_id']}, artist_names: {artist_names}, song_names: {song_names}")
        except Exception as e:
            print(f"[ERROR] 예상치 못한 오류 발생: {e}")
            print(f"[DEBUG] track 데이터: {track}")


    def upsert_lyrics(self, song_id, lyrics):
        """가사 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"lyrics": lyrics}},
            upsert=True
        )

    def upsert_translation(self, song_id, translated_lyrics):
        """번역된 가사 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"translated_lyrics": translated_lyrics}},
            upsert=True
        )

    def upsert_phonetics(self, song_id, phonetics):
        """발음 데이터 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"phonetics_lyrics": phonetics}},
            upsert=True
        )

    def upsert_phonetics_korean(self, song_id, phonetics_korean):
        """한국어 발음 데이터 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"phonetics_korean_lyrics": phonetics_korean}},
            upsert=True
        )
    
    def upsert_kanji_info(self, song_id, kanji_info):
        """한국어 발음 데이터 삽입 또는 업데이트"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$set": {"kanji_info": kanji_info}},
            upsert=True
        )

    def insert_song_name(self, song_id, song_name):
        """곡에 새로운 이름 추가 (한국어 또는 기타 언어 포함)"""
        self.collection.update_one(
            {"song_id": song_id},
            {"$addToSet": {"song_names": song_name}},  # 리스트에 추가 (중복 방지)
            upsert=True
        )

    def find_song_by_id(self, song_id):
        """곡 ID로 곡 정보 조회"""
        return self.collection.find_one({"song_id": song_id})

    def find_song_by_artist_id(self, artist_id, song_name):
        song = self.collection.find_one({"artist_id": artist_id, "song_names": song_name})
        if song :
            return song
        else:
            return None


    def find_song_by_artist_name(self, artist_name, song_name):
        """아티스트 이름과 곡명으로 곡 정보 조회 (리스트 내에서 검색)"""
        song =  self.collection.find_one({
            "artist_names": artist_name,
            "song_names": song_name
        })
        
        if song : 
            return song
        else : 
            return None
        

    def find_translated_lyrics(self, song_id):
        """번역된 가사 조회"""
        song = self.collection.find_one({"song_id": song_id}, {"translated_lyrics": 1})
        return song["translated_lyrics"] if song and "translated_lyrics" in song else None

    def find_kanji_info(self, song_id):
        """곡의 한자 정보 조회"""
        song = self.collection.find_one({"song_id" : song_id}, {"kanji_info": 1})
        return song["kanji_info"] if song and "kanji_info" in song else None