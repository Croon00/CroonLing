from database.songs_db import SongsDB


class SongService:
    def __init__(self):
        self.songs_db = SongsDB()

    def get_song_info(self, artist, song):
        """
        특정 곡의 정보 가져오기
        :param artist: 가수 이름
        :param song: 곡 제목
        :return: 곡 정보 딕셔너리 또는 None
        """
        song_info = self.songs_db.find_song_by_id(artist, song)
        if song_info:
            return {
                "song_name": song_info["song_name"],
                "artist_name": song_info["artist_name"],
                "album_name": song_info.get("album_name", None),
                "track_image_url": song_info.get("track_image_url", None),
                "release_date": song_info.get("release_date", None),
            }
        # 정보가 없을 경우 None 반환
        return None
    
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

