from apis import SpotifyAPI

class SpotifyService:
    def __init__(self):
        self.spotify_api = SpotifyAPI()

    async def get_artist_info(self, artist_name):
        """Spotify에서 아티스트 검색"""
        search_result = await self.spotify_api.search(artist_name, search_type="artist")
        artists = search_result.get('artists', {}).get('items', [])
        if not artists:
            return None
        artist = artists[0]
        return {
            "artist_id": artist["id"],
            "artist_name": artist["name"]
        }

    async def get_albums_by_artist(self, artist_id):
        """아티스트의 앨범 목록 가져오기"""
        albums_result = await self.spotify_api.get(
            f"artists/{artist_id}/albums",
            params={"include_groups": "album", "limit": 50}
        )
        return albums_result.get('items', [])

    async def get_singles_by_artist(self, artist_id):
        """아티스트의 싱글 목록 가져오기"""
        singles_result = await self.spotify_api.get(
            f"artists/{artist_id}/albums",
            params={"include_groups": "single", "limit": 50}
        )
        return singles_result.get('items', [])

    async def get_all_songs_by_artist(self, artist_id):
        """아티스트의 모든 곡 목록 가져오기 (앨범 + 싱글)"""
        albums = await self.get_albums_by_artist(artist_id)
        singles = await self.get_singles_by_artist(artist_id)
        all_tracks = []
        for album in albums + singles:
            album_tracks_result = await self.spotify_api.get(f"albums/{album['id']}/tracks")
            tracks = album_tracks_result.get('items', [])
            all_tracks.extend([
                {
                    "song_name": track["name"],
                    "album_name": album["name"],
                    "release_date": album["release_date"]
                }
                for track in tracks
            ])
        return all_tracks

    async def search_song(self, artist_name, song_name):
        """Spotify에서 특정 곡 검색"""
        query = f"track:{song_name} artist:{artist_name}"
        search_result = await self.spotify_api.search(query, search_type="track")
        tracks = search_result.get('tracks', {}).get('items', [])
        if not tracks:
            return None
        track = tracks[0]
        return {
            "song_id": track["id"],
            "song_name": track["name"],
            "artist_name": track["artists"][0]["name"],
            "album_name": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "track_image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            "spotify_url": track["external_urls"]["spotify"]
        }
        
    async def get_track_popularity(self, track_id):
        """트랙의 인기도 가져오기"""
        track_result = await self.spotify_api(f"tracks/{track_id}")
        if not track_result:
            return None
        
        popularity = track_result.get("popularity", 0) # 0 ~ 100 사이 값
        
        # ✅ 인기도 설명 추가
        if popularity >= 80:
            popularity_status = "🔥 매우 인기 있는 곡!"
        elif popularity >= 60:
            popularity_status = "🎶 인기 있는 곡"
        elif popularity >= 40:
            popularity_status = "🎵 어느 정도 알려진 곡"
        else:
            popularity_status = "🔍 숨겨진 명곡"

        return {
            "song_name": track_result["name"],
            "artist_name": track_result["artists"][0]["name"],
            "popularity": popularity,
            "popularity_status": popularity_status
        }
    
    
    async def get_related_artists(self, artist_id):
        """유사한 아티스트 추천"""
        related_result = await self.spotify_api.get(f"artists/{artist_id}/related-artists")
        related_artists = related_result.get('artists', [])

        return [
            {
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "popularity": artist["popularity"],
                "genres": artist["genres"]
            }
            for artist in related_artists[:5]  # ✅ 상위 5명만 반환
        ]

    async def get_recommendations(self, track_id):
        """유사한 트랙 추천"""
        recommendations = await self.spotify_api.get(
            "recommendations",
            params={"seed_tracks": track_id, "limit": 5}  # ✅ 최대 5곡 추천
        )
        recommended_tracks = recommendations.get('tracks', [])

        return [
            {
                "song_name": track["name"],
                "artist_name": track["artists"][0]["name"],
                "popularity": track["popularity"],
                "spotify_url": track["external_urls"]["spotify"]
            }
            for track in recommended_tracks
        ]