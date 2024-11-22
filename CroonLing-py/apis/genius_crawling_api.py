import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from .api_interface import APIInterface

class GeniusCrawler(APIInterface):
    def __init__(self):
        # 현재 파일의 디렉토리 기준으로 chromedriver 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.driver_path = os.path.join(current_dir, "chromedriver.exe")
        self.service = Service(self.driver_path)
        self.driver = None

    def start_browser(self):
        # WebDriver 실행
        self.driver = webdriver.Chrome(service=self.service)

    def request(self, url):
        """
        APIInterface의 request 메서드를 구현하여 가사를 가져오는 기능 수행
        - url: 가사를 가져올 페이지 URL (string)
        """
        if not self.driver:
            self.start_browser()
        self.driver.get(url)
        time.sleep(5)
        
        # data-lyrics-container 속성을 가진 요소들을 가져와서 가사 텍스트 추출
        lyrics_container = self.driver.find_elements(By.XPATH, '//div[@data-lyrics-container="true"]')
        lyrics = [element.text for element in lyrics_container]

        return "\n".join(lyrics)

    def close_browser(self):
        # 브라우저 종료
        if self.driver:
            self.driver.quit()
