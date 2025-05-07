import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import logging
import time
import random
from database import LyricsDB
from config_loader import load_config
import os
from pyvirtualdisplay import Display

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LyricsService:
    def __init__(self):
        config = load_config()
        self.lyrics_db = LyricsDB()
        self.logger = logging.getLogger(__name__)

    # ✅ 추가된 부분
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
        self.logger.info(f"🔍 가사 검색 시작: {artist_name} - {song_name}")

        query = f"{artist_name} {song_name} lyrics"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        # ✅ Chrome 옵션 설정
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")

        # ✅ 환경변수에서 크롬 및 드라이버 경로 가져오기
        chrome_binary = os.getenv('CHROME_BINARY', '/usr/bin/google-chrome')
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')

        # ✅ 가상 디스플레이 시작 (Headless 환경 대체)
        display = Display(visible=0, size=(1920, 1080))
        display.start()

        driver = None
        try:
            driver = uc.Chrome(
                options=options,
                browser_executable_path=chrome_binary,
                driver_executable_path=chromedriver_path
            )
            
            self.logger.debug(f"📡 Google 검색 요청: {query}")
            
            # 페이지 로드
            driver.get(url)
            driver.implicitly_wait(10)
            time.sleep(random.uniform(3, 5))

            # 페이지 끝까지 반복 스크롤
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # HTML 가져오기
            html_content = driver.page_source
            lyrics = self._extract_lyrics_from_google(html_content)

            if lyrics:
                self.logger.info("✅ 가사 추출 및 저장 완료")
                lyrics_text = "\n".join(lyrics)
                await self.lyrics_db.upsert_lyrics(song_id, lyrics_text)
                return lyrics_text
            else:
                self.logger.warning("⚠️ 유효한 가사를 찾지 못했습니다.")
                return None

        except Exception as e:
            self.logger.exception(f"❌ 가사 추출 과정 중 오류 발생: {e}")
            return None

        finally:
            if driver:
                driver.quit()
            display.stop()
            time.sleep(random.uniform(1, 3))

    def _extract_lyrics_from_google(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            lyrics_elements = soup.find_all('div', class_='BNeawe tAd8D AP7Wnd')
            if not lyrics_elements:
                self.logger.warning("⚠️ 가사 요소를 찾을 수 없습니다.")
                return None
            
            lyrics = [element.get_text().strip() for element in lyrics_elements]
            return lyrics

        except Exception as e:
            self.logger.exception(f"❌ Google 가사 파싱 오류: {e}")
            return None
