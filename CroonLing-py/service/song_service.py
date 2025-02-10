import requests
import re
from database import SongsDB, ArtistsDB

class SongService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.artists_db = ArtistsDB()  # 아티스트 저장을 위한 DB 연결 추가

    def get_song_info(self, artist_name, song_name):
        """
        특정 곡의 정보 가져오기
        """
        song_info = self.songs_db.find_song_by_artist(artist_name, song_name)
        if song_info:
            return {
                "song_name": song_info["song_name"],
                "artist_name": song_info["artist_name"],
                "album_name": song_info.get("album_name"),
                "track_image_url": song_info.get("track_image_url"),
                "release_date": song_info.get("release_date"),
            }
        return None

    def save_track(self, track):
        """
        곡을 DB에 저장 (아티스트도 함께 저장)
        """
        artist_id = track["artist_id"]
        artist_name = track["artist_name"]

        # 아티스트 저장 여부 확인 및 저장
        if not self.artists_db.find_artist_id(artist_id):
            self.artists_db.upsert_artist(artist_id, artist_name)

        # 곡 저장 여부 확인 후 저장
        if not self.songs_db.find_song_by_artist(track["artist_name"], track["song_name"]):
            self.songs_db.upsert_song(track)

    def fetch_youtube_url(self, artist_name, song_name):
        """
        YouTube에서 곡 검색 후 첫 번째 영상 URL 반환
        """
        query = f"{artist_name} {song_name}"
        search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
            if video_ids:
                return f"https://www.youtube.com/watch?v={video_ids[0]}"
        except requests.RequestException as e:
            print(f"YouTube 검색 중 오류 발생: {e}")

        return None
