import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from database import LyricsDB

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LyricsService:
    def __init__(self):
        self.lyrics_db = LyricsDB()
        self.logger = logging.getLogger(__name__)

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

        search_query = f"{artist_name} {song_name} lyrics"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        self.logger.debug(f"🔗 검색 URL: {search_url}")

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = None
        try:
            self.logger.info("🚀 Chrome WebDriver 실행 중...")
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)

            driver.get(search_url)
            self.logger.info("✅ 페이지 요청 완료")

            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ujudUb')]/span"))
            )

            self.logger.info("✅ 가사 요소 발견 완료")

            # 페이지 저장 (디버깅용)
            with open("lyrics_result.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            lyrics_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'ujudUb')]")
            if not lyrics_divs:
                self.logger.warning("⚠️ 가사 div 찾기 실패")
                return None

            lyrics = "\n".join(span.text for div in lyrics_divs for span in div.find_elements(By.TAG_NAME, "span"))

            if lyrics.strip():
                self.logger.info("✅ 가사 추출 성공")
                await self.lyrics_db.upsert_lyrics(song_id, lyrics.strip())
                return lyrics.strip()
            else:
                self.logger.warning("⚠️ 빈 가사 텍스트")
                return None

        except (TimeoutException, NoSuchElementException):
            self.logger.error("❌ 요소 로딩 실패 - 가사 못 찾음")
        except WebDriverException as e:
            self.logger.exception(f"🚨 WebDriver 오류 발생: {e}")
        except Exception as e:
            self.logger.exception(f"❌ 예외 발생: {e}")
        finally:
            if driver:
                driver.quit()
                self.logger.info("🛑 Chrome WebDriver 종료")

        return None
