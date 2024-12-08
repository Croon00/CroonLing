from database.db_manager import DBManager


class InfoHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def get_song_info(self, artist, song):
        """
        특정 곡의 정보 가져오기
        """
        song_info = self.db_manager.get_song_info(artist, song)
        if song_info:
            return {
                "song_name": song_info["song_name"],
                "artist_name": song_info["artist_name"],
                "album_image": song_info["album_image"],
                "release_date": song_info["release_date"],
                "popularity": song_info["popularity"],
                "youtube_link": song_info["youtube_link"]
            }
        return "해당 곡 정보가 없습니다."
