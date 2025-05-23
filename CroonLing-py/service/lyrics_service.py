import logging
import httpx
from database import LyricsDB
from config_loader import load_config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LyricsService:
    def __init__(self):
        config = load_config()
        self.lyrics_db = LyricsDB()
        self.logger = logging.getLogger(__name__)
        self.gcp_crawler_url = f"http://{config['GCP_CRAWLER_IP']}:{config['GCP_CRAWLER_PORT']}/api/v1/lyrics"

    async def get_lyrics(self, song_id):
        """
        MongoDB에서 가사를 조회합니다.
        """
        try:
            self.logger.info(f"🔍 가사 조회 시작 - ID: {song_id}")
            data = await self.lyrics_db.find_lyrics_by_id(song_id)
            if data and "lyrics" in data:
                self.logger.info(f"✅ 가사 조회 성공 - ID: {song_id}")
                return data["lyrics"]
            else:
                self.logger.warning(f"⚠️ 가사 없음 - ID: {song_id}")
                return None
        except Exception as e:
            self.logger.exception(f"❌ 가사 검색 중 오류 발생: {e}")
            return None

    async def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        """
        GCP VM에 배포된 크롤러 API에 요청하여 가사를 가져옵니다.
        """
        self.logger.info(f"🔍 GCP 크롤러에 가사 요청: {artist_name} - {song_name}")
        start_time = time.time()

        try:
            timeout = httpx.Timeout(30.0, connect=10.0)  # ✅ timeout 명시적으로 증가

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(self.gcp_crawler_url, json={
                    "artist_name": artist_name,
                    "song_name": song_name
                })

            elapsed = time.time() - start_time
            self.logger.info(f"📦 GCP 응답 시간: {elapsed:.2f}초")

            if response.status_code == 200:
                data = response.json()
                lyrics = data.get('lyrics')
                
                if lyrics:
                    self.logger.info("✅ 가사 요청 성공, DB에 저장합니다.")
                    await self.lyrics_db.upsert_lyrics(song_id, lyrics)
                    return lyrics
                else:
                    self.logger.warning("⚠️ 가사를 찾지 못했습니다.")
                    return None
            else:
                self.logger.warning(f"⚠️ GCP 요청 실패: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.exception(f"❌ GCP VM 요청 중 오류 발생 (소요 시간: {elapsed:.2f}초): {e}")
            return None
