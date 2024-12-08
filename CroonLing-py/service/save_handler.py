from database.db_manager import DBManager


class SaveHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def save_artist_and_songs(self, artist, album, songs):
        """
        DB에 artist, album, 그리고 songs 저장
        이미 저장된 트랙이 있을 경우 알림
        """
        saved_tracks = []
        duplicate_tracks = []
        for song in songs:
            if not self.db_manager.is_song_saved(artist, song):
                self.db_manager.insert_song(artist, album, song)
                saved_tracks.append(song)
            else:
                duplicate_tracks.append(song)

        return {
            "saved_tracks": saved_tracks,
            "duplicate_tracks": duplicate_tracks
        }
