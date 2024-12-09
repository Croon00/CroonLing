from database.base_db import BaseDB
from pymysql import MySQLError

class ArtistsDB(BaseDB):
    def get_artist_id(self, artist_name):
        """아티스트 ID 조회 또는 추가"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT artist_id FROM artists WHERE artist_name = %s"
                cursor.execute(query, (artist_name,))
                result = cursor.fetchone()

                if result:
                    return result[0]

                # 없으면 추가
                insert_query = "INSERT INTO artists (artist_name) VALUES (%s)"
                cursor.execute(insert_query, (artist_name,))
                connection.commit()
                return cursor.lastrowid
        except MySQLError as e:
            print(f"Get artist ID error: {str(e)}")
        finally:
            connection.close()

    def insert_artist_name_kr(self, artist_id, korean_artist_name):
        """한국어 아티스트 이름 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO artist_kr (artist_id, artist_kr_name)
                VALUES (%s, %s)
                """
                cursor.execute(query, (artist_id, korean_artist_name))
                connection.commit()
        except MySQLError as e:
            print(f"Insert artist name KR error: {str(e)}")
        finally:
            connection.close()
