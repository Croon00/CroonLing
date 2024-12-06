from pymysql import connect
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

    def insert_song(self, artist, song, lyrics):
        """가수와 곡 정보를 삽입"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO songs (artist, song, lyrics)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (artist, song, lyrics))
                connection.commit()
        except Exception as e:
            print(f"Insert song error: {str(e)}")
        finally:
            connection.close()

    def get_lyrics(self, artist, song):
        """가사 정보 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                select_query = """
                SELECT lyrics, translated_lyrics, phonetics_lyrics, korean_phonetics_lyrics 
                FROM songs WHERE artist = %s AND song = %s
                """
                cursor.execute(select_query, (artist, song))
                result = cursor.fetchone()
                if result:
                    return result  # lyrics, translated_lyrics, phonetics_lyrics, korean_phonetics_lyrics
                return None, None, None, None
        except Exception as e:
            print(f"Get lyrics error: {str(e)}")
            return None, None, None, None
        finally:
            connection.close()

    def update_translation(self, artist, song, translated_lyrics):
        """번역된 가사 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET translated_lyrics = %s WHERE artist = %s AND song = %s
                """
                cursor.execute(update_query, (translated_lyrics, artist, song))
                connection.commit()
        except Exception as e:
            print(f"Update translation error: {str(e)}")
        finally:
            connection.close()

    def update_phonetics(self, artist, song, phonetics_lyrics):
        """로마자 발음 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET phonetics_lyrics = %s WHERE artist = %s AND song = %s
                """
                cursor.execute(update_query, (phonetics_lyrics, artist, song))
                connection.commit()
        except Exception as e:
            print(f"Update phonetics error: {str(e)}")
        finally:
            connection.close()

    def update_korean(self, artist, song, korean_phonetics_lyrics):
        """한글 발음 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET korean_phonetics_lyrics = %s WHERE artist = %s AND song = %s
                """
                cursor.execute(update_query, (korean_phonetics_lyrics, artist, song))
                connection.commit()
        except Exception as e:
            print(f"Update korean_phonetics_lyrics error: {str(e)}")
        finally:
            connection.close()
