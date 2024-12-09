from database.songs_db import SongsDB


class GetInfoHandler:
    def __init__(self):
        self.songs_db = SongsDB()

    def get_song_info(self, artist, song):
        """
        특정 곡의 정보 가져오기
        :param artist: 가수 이름
        :param song: 곡 제목
        :return: 곡 정보 딕셔너리 또는 None
        """
        song_info = self.songs_db.get_song_info(artist, song)
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
