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
from database.songs_db import SongsDB

# ✅ 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG 레벨부터 기록
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LyricsService:
    def __init__(self):
        self.songs_db = SongsDB()  # ✅ 기존 DB 연결 유지
        self.logger = logging.getLogger(__name__)  # ✅ 클래스 내 로깅 객체 생성

    def get_lyrics(self, song_id):
        """곡의 가사 반환"""
        try:
            song = self.songs_db.find_song_by_id(song_id)
            if song:
                self.logger.info(f"✅ 가사 조회 성공 (ID: {song_id})")
                return song.get("lyrics")
            else:
                self.logger.warning(f"⚠️ 가사 없음 (ID: {song_id})")
                return None
        except Exception as e:
            self.logger.exception(f"❌ 가사 검색 중 오류 발생: {e}")
            return None

    def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        """Selenium을 사용하여 구글에서 가사를 검색하고 저장"""
        self.logger.info(f"🔍 가사 검색 시작: {artist_name} - {song_name}")

        search_query = f"{artist_name} {song_name} lyrics"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        self.logger.debug(f"🔗 검색 URL: {search_url}")

        # ✅ Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # GUI 없이 실행
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

        # ✅ 자동화 탐지 방지 옵션 추가
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = None
        try:
            self.logger.info("🚀 Chrome WebDriver 실행 중...")
            service = Service("/usr/bin/chromedriver")  # ✅ 크롬 드라이버 경로
            driver = webdriver.Chrome(service=service, options=chrome_options)

            driver.get(search_url)
            self.logger.info("✅ 페이지 요청 완료")

            # ✅ 페이지가 완전히 로딩될 때까지 대기 (최대 30초)
            time.sleep(5)  # 🚀 5초 대기 후 요소 탐색 시작
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ujudUb")))
            self.logger.info("✅ 페이지 로드 완료!")

            # ✅ 가사 컨테이너 찾기
            lyrics_divs = driver.find_elements(By.CLASS_NAME, "ujudUb")

            if not lyrics_divs:
                self.logger.warning("⚠️ 가사 정보를 찾을 수 없습니다.")
                return None

            # ✅ 각 div 안에서 <span jsname="YS01Ge"> 태그들의 텍스트 수집
            lyrics = "\n".join(span.text for div in lyrics_divs for span in div.find_elements(By.TAG_NAME, "span"))

            if lyrics.strip():
                self.logger.info("✅ 가사 가져옴!")
                self.songs_db.upsert_lyrics(song_id, lyrics.strip())  # ✅ 기존 DB 구조 유지
                return lyrics.strip()
            else:
                self.logger.warning("⚠️ 가사 정보를 가져오지 못했습니다.")
                return None

        except TimeoutException:
            self.logger.error("⏳ 페이지 로딩 시간 초과")
        except NoSuchElementException:
            self.logger.error("❌ 요소를 찾을 수 없음")
        except WebDriverException as e:
            self.logger.exception(f"🚨 WebDriver 오류 발생: {e}")
        except Exception as e:
            self.logger.exception(f"❌ 예상치 못한 오류 발생: {e}")
        finally:
            if driver:
                driver.quit()
                self.logger.info("🛑 Chrome WebDriver 종료")

        return None
