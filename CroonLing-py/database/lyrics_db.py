from database.base_db import BaseDB
from pymysql import MySQLError


class LyricsDB(BaseDB):
    def insert_lyrics(self, artist_name, song_name, lyrics):
        """
        곡의 기본 가사를 삽입
        :param artist_name: 가수 이름
        :param song_name: 곡 제목
        :param lyrics: 삽입할 가사
        :raises ValueError: 아티스트 또는 곡이 존재하지 않을 경우
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                
                
                cursor.execute(
                    "SELECT * FROM artists"
                )
                temp = cursor.fetchone()
                
                
                # 아티스트 ID 가져오기
                cursor.execute(
                    "SELECT artist_id FROM artists WHERE artist_name = %s", (artist_name,)
                )
                artist_result = cursor.fetchone()

                
                if not artist_result:
                    raise ValueError(f"'{artist_name}'는 데이터베이스에 존재하지 않습니다.")

                artist_id = artist_result[0]
                

                # 곡 ID 가져오기
                cursor.execute(
                    "SELECT song_id FROM songs WHERE artist_id = %s AND song_name = %s",
                    (artist_id, song_name),
                )
                song_result = cursor.fetchone()
                

                if not song_result:
                    raise ValueError(f"'{song_name}'는 데이터베이스에 존재하지 않습니다.")

                song_id = song_result[0]

                # 기본 가사 삽입
                cursor.execute(
                    "UPDATE songs SET lyrics = %s WHERE song_id = %s",
                    (lyrics, song_id),
                )
                connection.commit()

        except MySQLError as e:
            print(f"Insert lyrics error: {str(e)}")
        finally:
            connection.close()

    def get_lyrics(self, song_id):
        """
        곡의 가사를 조회
        :param artist_name: 가수 이름
        :param song_name: 곡 제목
        :return: 저장된 가사 또는 None
        """
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT lyrics
                    FROM songs s
                    WHERE song_id = %s
                    """,
                    (song_id),
                )
                result = cursor.fetchone()
                return result[0] if result else None

        except MySQLError as e:
            print(f"Get lyrics error: {str(e)}")
            return None
        finally:
            connection.close()
