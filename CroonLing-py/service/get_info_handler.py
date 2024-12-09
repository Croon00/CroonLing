from database.songs_db import SongsDB


class GetInfoHandler:
    def __init__(self):
        self.songs_db = SongsDB()

    def get_song_info(self, artist, song):
        """
        특정 곡의 정보 가져오기
        """
        song_info = self.songs_db.get_song_info(artist, song)
        if song_info:
            return {
                "song_name": song_info["song_name"],
                "artist_name": song_info["artist_name"],
                "album_name": song_info.get("album_name", "N/A"),
                "track_image": song_info.get("track_image_url", "N/A"),
                "release_date": song_info.get("release_date", "N/A"),
            }
        return "해당 곡 정보가 없습니다."
