import requests
from bs4 import BeautifulSoup

class GoogleLyrics:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_lyrics(self, artist, song):
        """구글에서 가사 검색"""
        search_query = f"{artist} {song} lyrics"
        search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"

        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"구글 검색 중 오류가 발생했습니다: {str(e)}")

        soup = BeautifulSoup(response.text, "html.parser")

        # 가사 부분의 여러 섹션들을 모두 탐색
        lyrics_divs = soup.find_all("div", class_="ujudUb")
        if not lyrics_divs:
            return None

        lyrics = ""
        for div in lyrics_divs:
            spans = div.find_all("span", jsname="YS01Ge")
            for span in spans:
                lyrics += span.text + "\n"
            lyrics += "\n"

        return lyrics.strip() if lyrics.strip() else None
