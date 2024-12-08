from database.db_manager import DBManager


class SongNameHandler:
    def __init__(self):
        self.db_manager = DBManager()

    def update_song_name(self, song_id, new_name):
        """
        곡 이름 업데이트
        """
        result = self.db_manager.update_song_name(song_id, new_name)
        if result:
            return f"곡 이름이 '{new_name}'으로 업데이트되었습니다."
        return "곡 이름 업데이트에 실패했습니다."
