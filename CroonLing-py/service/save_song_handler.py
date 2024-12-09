from database.songs_db import SongsDB


class SaveHandler:
    def __init__(self):
        self.songs_db = SongsDB()  # SongsDB를 사용하여 곡 관련 DB 작업 처리

    def save_tracks(self, track_list):
        """
        DB에 tracks 저장
        이미 저장된 트랙이 있을 경우 알림

        Parameters:
        - track_list: 트랙 정보 리스트 (각 요소는 딕셔너리)
          - artist_name: 아티스트 이름
          - album_name: 앨범 이름 (없으면 None)
          - song_id: 트랙 ID
          - song_title: 트랙 제목
          - release_date: 발매일
          - track_image_url: 트랙 이미지 URL

        Returns:
        - 저장된 트랙과 중복된 트랙 정보를 반환
        """
        saved_tracks = []
        duplicate_tracks = []

        for track in track_list:
            # 곡이 이미 저장되어 있는지 확인
            if not self.songs_db.is_song_saved(track["artist_name"], track["song_title"]):
                # 곡을 DB에 삽입
                self.songs_db.insert_song(track)
                saved_tracks.append(track)
            else:
                # 중복된 곡으로 처리
                duplicate_tracks.append(track)

        return {
            "saved_tracks": saved_tracks,
            "duplicate_tracks": duplicate_tracks,
        }
