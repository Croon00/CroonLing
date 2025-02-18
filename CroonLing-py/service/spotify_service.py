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
