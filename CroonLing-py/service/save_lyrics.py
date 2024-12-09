import requests
from bs4 import BeautifulSoup
from database.lyrics_db import LyricsDB


class SaveLyricsService:
    def __init__(self):
        self.lyrics_db = LyricsDB()

    def fetch_and_save_lyrics(self, artist_name, song_name):
        """
        구글에서 가사를 검색하여 데이터베이스에 저장하고 반환합니다.
        :param artist_name: 가수 이름
        :param song_name: 곡 이름
        :return: 검색된 가사 또는 None
        """
        search_query = f"{artist_name} {song_name} lyrics"
        search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"구글 검색 중 오류가 발생했습니다: {str(e)}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 가사 섹션 찾기
        lyrics_divs = soup.find_all("div", class_="ujudUb")
        if not lyrics_divs:
            return None

        # 가사 추출
        lyrics = ""
        for div in lyrics_divs:
            spans = div.find_all("span", jsname="YS01Ge")
            for span in spans:
                lyrics += span.text + "\n"
            lyrics += "\n"

        if lyrics.strip():
            # 가사를 데이터베이스에 저장
            self.lyrics_db.insert_lyrics(artist_name, song_name, lyrics.strip())
            return lyrics.strip()

        return None
