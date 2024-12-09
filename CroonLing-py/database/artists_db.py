from database.base_db import BaseDB
from pymysql import MySQLError

class ArtistsDB(BaseDB):
    def is_artist_saved(self, artist_id):
        """아티스트 저장 여부 확인"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT 1 FROM artists WHERE artist_id = %s"
                cursor.execute(query, (artist_id,))
                return cursor.fetchone() is not None
        except MySQLError as e:
            print(f"Check artist saved error: {str(e)}")
            return False
        finally:
            connection.close()

    def insert_artist_name(self, artist_id, artist_name):
        """아티스트 이름 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO artists (artist_id, artist_name)
                VALUES (%s, %s)
                """
                cursor.execute(query, (artist_id, artist_name))
                connection.commit()
        except MySQLError as e:
            print(f"Insert artist name error: {str(e)}")
        finally:
            connection.close()
