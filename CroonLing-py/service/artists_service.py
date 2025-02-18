from database.artists_db import ArtistsDB

class ArtistsService:
    def __init__(self):
        self.artists_db = ArtistsDB()

    def get_artist_info(self, artist_name):
        """아티스트 존재 여부 확인 (영어/한국어 이름 검색)"""
        artist = self.artists_db.find_artist_by_name(artist_name)
        if artist:
            return {
                "artist_id": artist["artist_id"],
                "artist_name": artist["artist_name"],
                "artist_kr": artist.get("artist_kr", []),
                "exists": True
            }
        return {"artist_name": artist_name, "exists": False}

    def save_artist(self, artist_id, artist_name):
        """Spotify에서 검색한 아티스트 저장"""
        self.artists_db.upsert_artist(artist_id, artist_name)
        return f"아티스트 '{artist_name}'(ID: {artist_id}) 정보가 저장되었습니다."

    def add_artist_kr_name(self, artist_name, korean_name):
        """기존 아티스트에 한국어 이름 추가"""
        artist = self.artists_db.find_artist_by_name(artist_name)
        if not artist:
            return {"success": False, "message": f"'{artist_name}' 가수를 찾을 수 없습니다."}

        artist_id = artist["artist_id"]
        success = self.artists_db.insert_artist_name_kr(artist_id, korean_name)
        if success:
            return {"success": True, "message": f"'{artist_name}'의 한국어 이름 '{korean_name}' 추가 완료"}
        else:
            return {"success": False, "message": f"'{artist_name}'이(가) 존재하지 않아 한국어 이름을 추가할 수 없습니다."}
