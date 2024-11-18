from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

class GeniusCrawler:
    def __init__(self):
        # 현재 파일의 디렉토리 기준으로 chromedriver 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.driver_path = os.path.join(current_dir, "chromedriver.exe")
        
        # Service 객체 생성
        self.service = Service(self.driver_path)
        self.driver = None
        
        def start_browser(self):
            # WebDriver 실행
            self.driver = webdriver.Chrome(service=self.service)
            
        def fetch_lyrics(self, url):
            # 브라우저 실행 및 페이지 로드
            self.driver.get(url)
            time.sleep(5)
            
            # data-lyrics-container 속성을 가진 요소 가져오기
            lyrics_container = self.driver.find(elements(By.XPATH, '//div[@data-lyrics-container="true"]'))
            
