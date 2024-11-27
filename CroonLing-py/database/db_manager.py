from pymysql import connect

from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

# database/db_manager.py 파일 생성 및 DBManager 클래스 정의
class DBManager:
    def __init__(self):
        self.config = config

    def insert_song(self, artist, song, lyrics):
        connection = connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )
        try:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO songs (artist, song, lyrics)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (artist, song, lyrics))
                connection.commit()
        finally:
            connection.close()
            
    def get_lyrics(self, artist, song):
        connection = connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )
        try:
            with connection.cursor() as cursor:
                select_query = """
                SELECT lyrics FROM songs WHERE artist = %s AND song = %s
                """
                cursor.execute(select_query, (artist, song))
                result = cursor.fetchone()
                return result[0] if result else None
        finally:
            connection.close()

    def update_translation(self, artist, song, translated_lyrics):
        connection = connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET translated_lyrics = %s WHERE artist = %s AND song = %s
                """
                cursor.execute(update_query, (translated_lyrics, artist, song))
                connection.commit()
        finally:
            connection.close()

    def update_phonetics(self, artist, song, phonetics_lyrics):
        connection = connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )
        try:
            with connection.cursor() as cursor:
                update_query = """
                UPDATE songs SET phonetics_lyrics = %s WHERE artist = %s AND song = %s
                """
                cursor.execute(update_query, (phonetics_lyrics, artist, song))
                connection.commit()
        finally:
            connection.close()