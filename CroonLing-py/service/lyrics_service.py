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
            # 배포 환경에 맞는 크롬드라이버 경로
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)

            driver.get(search_url)
            self.logger.info("✅ 페이지 요청 완료")

            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # 디버깅용 HTML 저장
            with open("lyrics_result.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
                self.logger.info("📝 디버깅용 HTML 저장 완료: lyrics_result.html")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 가사 div 선택: Google이 추출한 가사 정보는 특정 CSS 클래스를 가짐
            lyrics_divs = driver.find_elements(By.CSS_SELECTOR, "div.ilUpNd.d6Ejqe.aSRlid")
            lyrics = "\n".join(div.text.strip() for div in lyrics_divs if len(div.text.strip()) > 100)

            if lyrics:
                self.logger.info("✅ 가사 추출 성공")
                await self.lyrics_db.upsert_lyrics(song_id, lyrics.strip())
                return lyrics.strip()
            else:
                self.logger.warning("⚠️ 유효한 가사 블럭을 찾을 수 없습니다.")
                return None

        except TimeoutException:
            self.logger.error("⏳ 페이지 로딩 시간 초과")
        except NoSuchElementException:
            self.logger.error("❌ 요소를 찾을 수 없음")
        except WebDriverException as e:
            self.logger.exception(f"🚨 WebDriver 오류 발생: {e}")
        except Exception as e:
            self.logger.exception(f"❌ 예기치 못한 오류 발생: {e}")
        finally:
            if driver:
                driver.quit()
                self.logger.info("🛑 Chrome WebDriver 종료")

        return None
