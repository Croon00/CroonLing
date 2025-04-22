import requests
import logging
from bs4 import BeautifulSoup

from database import LyricsDB
from config_loader import load_config  # ✅ 추가

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LyricsService:
    def __init__(self):
        # ✅ 환경 변수 로드 방식 변경
        # config = load_config()
        self.lyrics_db = LyricsDB()
        self.logger = logging.getLogger(__name__)
        print("[DEBUG] SERPAPI_KEY =", os.getenv("SERPAPI_KEY"))
        self.serpapi_key = "763cccf333ef2f11902aa5ab8af334843fe23edf0b30394344c0893b9d5ef3a5"

    async def get_lyrics(self, song_id):
        try:
            data = await self.lyrics_db.find_lyrics_by_id(song_id)
            if data and "lyrics" in data:
                self.logger.info(f"✅ 가사 조회 성공 (ID: {song_id})")
                return data["lyrics"]
            else:
                self.logger.warning(f"⚠️ 가사 없음 (ID: {song_id})")
                return None
        except Exception as e:
            self.logger.exception(f"❌ 가사 검색 중 오류 발생: {e}")
            return None

    async def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        self.logger.info(f"🔍 가사 검색 시작: {artist_name} - {song_name}")

        if not self.serpapi_key:
            self.logger.error("❌ SERPAPI_KEY 설정이 누락되었습니다.")
            return None

        query = f"{artist_name} {song_name} lyrics site:genius.com"
        search_url = "https://serpapi.com/search"

        params = {
            "engine": "google",
            "q": query,
            "hl": "ja",
            "gl": "jp",
            "location": "Japan",
            "api_key": self.serpapi_key,
            "num": 5,
        }

        try:
            self.logger.debug(f"📡 SerpAPI 요청: {query}")
            response = requests.get(search_url, params=params, timeout=10)
            data = response.json()

            if response.status_code != 200 or "organic_results" not in data:
                self.logger.error("❌ SerpAPI 응답 오류 또는 결과 없음")
                return None

            genius_url = None
            for result in data["organic_results"]:
                url = result.get("link", "")
                if "genius.com" in url:
                    genius_url = url
                    break

            if not genius_url:
                self.logger.warning("⚠️ Genius 링크를 찾지 못했습니다.")
                return None

            self.logger.info(f"🎯 Genius 가사 페이지: {genius_url}")
            lyrics = self._extract_lyrics_from_genius(genius_url)

            if lyrics:
                self.logger.info("✅ 가사 추출 및 저장 완료")
                await self.lyrics_db.upsert_lyrics(song_id, lyrics)
                return lyrics
            else:
                self.logger.warning("⚠️ 유효한 가사를 찾지 못했습니다.")
                return None

        except Exception as e:
            self.logger.exception(f"❌ 가사 추출 과정 중 오류 발생: {e}")
            return None

    def _extract_lyrics_from_genius(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            containers = soup.select("div[data-lyrics-container='true']")
            if containers:
                lines = []
                for block in containers:
                    text = block.get_text(strip=True)
                    if len(text) < 10:
                        continue
                    lines.append(text)

                lyrics = "\n".join(lines)

                if "Lyrics" in lyrics:
                    lyrics = lyrics.split("Lyrics", 1)[-1].strip()

                return lyrics.strip()

            # fallback
            fallback = soup.select_one("div.lyrics")
            if fallback:
                return fallback.get_text(strip=True)

            return None

        except Exception as e:
            self.logger.exception(f"❌ Genius 가사 파싱 오류: {e}")
            return None
