from database import ArtistsDB

class ArtistsService:
    def __init__(self):
        self.artists_db = ArtistsDB()

    def get_artist(self, artist_id):
        """아티스트 존재 여부 확인 및 정보 조회"""
        artist = self.artists_db.find_artist_id(artist_id)
        if artist:
            return {"artist_id": artist_id, "exists": True}
        return {"artist_id": artist_id, "exists": False}

    def save_artist(self, artist_id, artist_name):
        """아티스트 정보 저장 (없으면 삽입, 있으면 업데이트)"""
        self.artists_db.upsert_artist(artist_id, artist_name)
        return f"아티스트 '{artist_name}'(ID: {artist_id}) 정보가 저장되었습니다."
