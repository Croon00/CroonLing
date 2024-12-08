from pymysql import connect, MySQLError
from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class DBManager:
    def __init__(self):
        self.config = config

    def _get_connection(self):
        """데이터베이스 연결 생성 메서드"""
        return connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )

    def insert_song(self, artist_id, song_id, lyrics):
        """곡 정보를 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO songs (artist_id, song_id, lyrics)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (artist_id, song_id, lyrics))
                connection.commit()
        except MySQLError as e:
            print(f"Insert song error: {str(e)}")
        finally:
            connection.close()

    def get_lyrics(self, artist_name, song_name):
        """가사 정보 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                select_query = """
                SELECT s.lyrics, s.translated_lyrics, s.phonetics_lyrics, s.korean_phonetics_lyrics
                FROM songs s
                JOIN artists a ON s.artist_id = a.artist_id
                WHERE a.artist_name = %s AND s.song_name = %s
                """
                cursor.execute(select_query, (artist_name, song_name))
                result = cursor.fetchone()
                return result if result else (None, None, None, None)
        except MySQLError as e:
            print(f"Get lyrics error: {str(e)}")
            return None, None, None, None
        finally:
            connection.close()

    def update_translation(self, song_id, translated_lyrics):
        """번역된 가사 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET translated_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(update_query, (translated_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update translation error: {str(e)}")
        finally:
            connection.close()

    def update_phonetics(self, song_id, phonetics_lyrics):
        """로마자 발음 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET phonetics_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(update_query, (phonetics_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update phonetics error: {str(e)}")
        finally:
            connection.close()

    def update_korean(self, song_id, korean_phonetics_lyrics):
        """한글 발음 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET korean_phonetics_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(update_query, (korean_phonetics_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update korean_phonetics_lyrics error: {str(e)}")
        finally:
            connection.close()

    def get_artist_info(self, artist_name):
        """가수 정보를 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT artist_id
                FROM artists
                WHERE artist_name = %s
                """
                cursor.execute(query, (artist_name,))
                return cursor.fetchone()
        except MySQLError as e:
            print(f"Get artist info error: {str(e)}")
            return None
        finally:
            connection.close()

    def insert_artist_name_kr(self, artist_id, korean_artist_name):
        """한국어 가수 이름을 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO artist_kr (artist_id, artist_kr_name)
                VALUES (%s, %s)
                """
                cursor.execute(query, (artist_id, korean_artist_name))
                connection.commit()
                return True
        except MySQLError as e:
            print(f"Insert artist name KR error: {str(e)}")
            return False
        finally:
            connection.close()

    def insert_song_name_kr(self, song_id, korean_song_name):
        """한국어 곡 이름을 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO songs_name_kr (song_id, song_name_kr)
                VALUES (%s, %s)
                """
                cursor.execute(query, (song_id, korean_song_name))
                connection.commit()
                return True
        except MySQLError as e:
            print(f"Insert song name KR error: {str(e)}")
            return False
        finally:
            connection.close()

    def is_song_saved(self, artist_name, song_name):
        """곡이 이미 저장되었는지 확인"""
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
