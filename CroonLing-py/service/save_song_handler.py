from database.songs_db import SongsDB
from database.artists_db import ArtistsDB

class SaveHandler:
    def __init__(self):
        self.songs_db = SongsDB()
        self.artists_db = ArtistsDB()

    def save_track(self, track):
        """
        DB에 트랙 저장
        Parameters:
        - track: 트랙 정보 딕셔너리
        """
        artist_id = track["artist_id"]
        artist_name = track["artist_name"]
        
        
        # 아티스트 저장 여부 확인 및 저장
        if not self.artists_db.is_artist_saved(artist_id):
            self.artists_db.insert_artist_name(artist_id, artist_name)
        
        
        # 곡 저장 여부 확인
        if not self.songs_db.is_song_saved(artist_name, track["song_name"]):
            self.songs_db.insert_song(
                {
                    "song_id": track["song_id"],
                    "song_name": track["song_name"],
                    "artist_id": track["artist_id"],
                    "release_date": track.get("release_date"),
                    "track_image_url": track.get("track_image_url"),
                    "album_name": track.get("album_name")
                }
            )
