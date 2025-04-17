from database import ArtistsDB
import logging
class ArtistsService:
    def __init__(self):
        self.artists_db = ArtistsDB()
        self.logger = logging.getLogger(__name__)

    async def get_artist_info(self, artist_name):
        artist = await self.artists_db.find_artist_by_name(artist_name)
        if artist:
            self.logger.info(f"✅ 아티스트 조회 성공: {artist_name}")
            return {
                "artist_id": artist["artist_id"],
                "artist_name": artist["artist_name"],
                "artist_kr": artist.get("artist_kr", []),
                "exists": True
            }
        self.logger.warning(f"⚠️ 아티스트 없음: {artist_name}")
        return {"artist_name": artist_name, "exists": False}

    async def save_artist(self, artist_id, artist_name):
        self.logger.info(f"🎵 아티스트 저장: {artist_name} (ID: {artist_id})")
        await self.artists_db.upsert_artist({"artist_id": artist_id, "artist_name": artist_name})
        return f"아티스트 '{artist_name}'(ID: {artist_id}) 정보가 저장되었습니다."

    async def add_artist_kr_name(self, artist_name, korean_name):
        artist = await self.artists_db.find_artist_by_name(artist_name)
        if not artist:
            return {"success": False, "message": f"'{artist_name}' 가수를 찾을 수 없습니다."}

        artist_id = artist["artist_id"]
        success = await self.artists_db.insert_artist_name_kr(artist_id, korean_name)
        if success:
            return {"success": True, "message": f"'{artist_name}'의 한국어 이름 '{korean_name}' 추가 완료"}
        else:
            return {"success": False, "message": f"'{artist_name}'이(가) 존재하지 않아 한국어 이름을 추가할 수 없습니다."}
