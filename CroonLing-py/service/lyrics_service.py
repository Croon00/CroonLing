from database.songs_db import SongsDB
import requests
from bs4 import BeautifulSoup

class LyricsService:
    def __init__(self):
        self.songs_db = SongsDB()

    def get_lyrics(self, song_id):
        """곡의 가사 반환"""
        song = self.songs_db.find_song_by_id(song_id)
        return song.get("lyrics") if song else None

    def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        """구글에서 가사를 검색하여 데이터베이스에 저장"""
        search_query = f"{artist_name} {song_name} lyrics"
        search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"구글 검색 중 오류 발생: {str(e)}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        lyrics_divs = soup.find_all("div", class_="ujudUb")
        lyrics = "\n".join(div.get_text("\n") for div in lyrics_divs) if lyrics_divs else None

        if lyrics:
            self.songs_db.upsert_lyrics(song_id, lyrics.strip())
            return lyrics.strip()

        return None
