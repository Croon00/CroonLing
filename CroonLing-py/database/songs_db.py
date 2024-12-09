from database.base_db import BaseDB
from pymysql import MySQLError

class SongsDB(BaseDB):
    def insert_song(self, track, artist_id):
        """곡 정보를 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO songs (song_id, artist_id, song_name, release_date, track_image_url, album_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    track["song_id"],
                    artist_id,
                    track["song_title"],
                    track["release_date"],
                    track["track_image_url"],
                    track.get("album_name"),
                ))
                connection.commit()
        except MySQLError as e:
            print(f"Insert song error: {str(e)}")
        finally:
            connection.close()

    def is_song_saved(self, artist_name, song_name):
        """곡 저장 여부 확인"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT 1
                FROM songs s
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = %s AND s.song_name = %s
                """
                cursor.execute(query, (artist_name, song_name))
                return cursor.fetchone() is not None
        finally:
            connection.close()

    def get_song_info(self, artist_name, song_name):
        """곡 정보 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT 
                    s.song_name, 
                    a.artist_name, 
                    s.album_name, 
                    s.track_image_url, 
                    s.release_date
                FROM songs s
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = %s AND s.song_name = %s
                """
                cursor.execute(query, (artist_name, song_name))
                result = cursor.fetchone()
                if result:
                    return {
                        "song_name": result[0],
                        "artist_name": result[1],
                        "album_name": result[2],
                        "track_image_url": result[3],
                        "release_date": result[4],
                    }
                return None
        except MySQLError as e:
            print(f"Get song info error: {str(e)}")
            return None
        finally:
            connection.close()
