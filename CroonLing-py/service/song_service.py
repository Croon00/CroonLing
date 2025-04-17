import requests
import re
from database import SongsDB, ArtistsDB
from apis import SpotifyAPI

class SongService:
    def __init__(self):
        self.songs_db = SongsDB()
        self.artists_db = ArtistsDB()
        self.spotify_api = SpotifyAPI()

    async def get_song_info(self, artist_id, song_name):
        song_info = await self.songs_db.find_song_by_artist_id(artist_id, song_name)
        if song_info:
            print("[DEBUG] 곡 정보 조회 성공")
            primary_song_name = song_info.get("song_names", [None])[0]
            primary_artist_name = song_info.get("artist_names", [None])[0]
            return {
                "song_name": primary_song_name if primary_song_name else song_name,
                "artist_name": primary_artist_name,
                "album_name": song_info.get("album_name"),
                "track_image_url": song_info.get("track_image_url"),
                "release_date": song_info.get("release_date"),
            }
        else:
            print("[DEBUG] 곡 정보 없음")
            return None

    async def get_song_info_by_artist_name(self, artist_name, song_name):
        song_info = await self.songs_db.find_song_by_artist_name(artist_name, song_name)
        return song_info if song_info else None

    async def save_track(self, track):
        artist_id = track["artist_id"]
        artist_name = track["artist_name"]

        existing_artist = await self.artists_db.find_artist_by_id(artist_id)
        if not existing_artist:
            artist_info = await self.spotify_api.get_artist_info(artist_id)
            if artist_info:
                await self.artists_db.upsert_artist(artist_info)

        song_exists = await self.songs_db.find_song_by_artist_id(track["artist_id"], track["song_name"])
        if not song_exists:
            await self.songs_db.upsert_song(track)

    async def fetch_youtube_url(self, artist_name, song_name):
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

