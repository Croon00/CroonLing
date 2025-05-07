    async def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        self.logger.info(f"🔍 가사 검색 시작: {artist_name} - {song_name}")

        query = f"{artist_name} {song_name} lyrics"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        # undetected-chromedriver 설정
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")  # ✅ "new" 옵션 제거
        options.add_argument("--remote-debugging-port=9222")  # ✅ 디버그 포트 설정
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")

        # ✅ ChromeDriver 강제 경로 지정
        driver = None
        try:
            driver = uc.Chrome(options=options, browser_executable_path="/usr/bin/chromium", use_subprocess=True)
            self.logger.debug(f"📡 Google 검색 요청: {query}")
            
            # 페이지 로드
            driver.get(url)
            driver.implicitly_wait(10)
            time.sleep(random.uniform(3, 5))  # 페이지 로드 대기

            # 페이지 끝까지 반복 스크롤
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # 스크롤 후 로딩 대기

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
                driver.quit()  # 브라우저 종료
            time.sleep(random.uniform(1, 3))  # 요청 간 대기
