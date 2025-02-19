from database.songs_db import SongsDB
import requests
from bs4 import BeautifulSoup

class LyricsService:
    def __init__(self):
        self.songs_db = SongsDB()  # ✅ 기존 구조 유지

    def get_lyrics(self, song_id):
        """곡의 가사 반환"""
        song = self.songs_db.find_song_by_id(song_id)
        return song.get("lyrics") if song else None

    def fetch_and_save_lyrics(self, song_id, artist_name, song_name):
        """구글에서 가사를 검색하여 데이터베이스에 저장"""
        print(f"[DEBUG] 가사 검색 시작: {artist_name} - {song_name}")

        search_query = f"{artist_name} {song_name} lyrics"
        search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] 구글 검색 중 오류 발생: {str(e)}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ 가사 컨테이너 찾기
        lyrics_container = soup.find("div", {"data-attrid": "kc:/music/recording_cluster:lyrics"})

        if not lyrics_container:
            print("[❌] 가사 정보를 찾을 수 없습니다. 다른 방식 시도")
            return None

        # ✅ 가사 텍스트 추출
        lyrics = "\n".join(span.text for span in lyrics_container.find_all("span", jsname="YS01Ge"))

        if lyrics:
            print("[✅] 가사 가져옴")
            self.songs_db.upsert_lyrics(song_id, lyrics.strip())  # ✅ 기존 DB 구조 유지
            return lyrics.strip()
        else:
            print("[❌] 가사 정보를 가져오지 못했습니다. 다른 방식 시도")
            return None
