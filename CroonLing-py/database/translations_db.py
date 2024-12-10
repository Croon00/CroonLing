from database.base_db import BaseDB
from pymysql import MySQLError

class TranslationsDB(BaseDB):
    def update_translation(self, song_id, translated_lyrics):
        """번역된 가사 삽입 또는 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                UPDATE songs SET translated_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(query, (translated_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update translation error: {str(e)}")
        finally:
            connection.close()

    def update_phonetics(self, song_id, phonetics_lyrics):
        """로마자 발음 삽입 또는 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                UPDATE songs SET phonetics_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(query, (phonetics_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update phonetics error: {str(e)}")
        finally:
            connection.close()

    def update_korean_phonetics(self, song_id, korean_phonetics_lyrics):
        """한국어 발음 삽입 또는 업데이트"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                UPDATE songs SET korean_phonetics_lyrics = %s WHERE song_id = %s
                """
                cursor.execute(query, (korean_phonetics_lyrics, song_id))
                connection.commit()
        except MySQLError as e:
            print(f"Update Korean phonetics error: {str(e)}")
        finally:
            connection.close()

    def get_translated_lyrics(self, song_id):
        """번역된 가사 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT translated_lyrics
                FROM songs
                WHERE song_id = %s
                """
                cursor.execute(query, (song_id))
                result = cursor.fetchone()
                return result[0] if result else None
        except MySQLError as e:
            print(f"Get translated lyrics error: {str(e)}")
            return None
        finally:
            connection.close()

    def get_phonetics(self, song_id):
        """로마자 발음 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT phonetics_lyrics
                FROM songs 
                WHERE song_id = %s
                """
                cursor.execute(query, (song_id))
                result = cursor.fetchone()
                return result[0] if result else None
        except MySQLError as e:
            print(f"Get phonetics error: {str(e)}")
            return None
        finally:
            connection.close()

    def get_korean_phonetics(self, song_id):
        """한국어 발음 조회"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT korean_phonetics_lyrics
                FROM songs 
                WHERE song_id = %s
                """
                cursor.execute(query, (song_id))
                result = cursor.fetchone()
                return result[0] if result else None
        except MySQLError as e:
            print(f"Get Korean phonetics error: {str(e)}")
            return None
        finally:
            connection.close()
