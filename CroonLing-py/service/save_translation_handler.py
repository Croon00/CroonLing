# from database.translations_db import TranslationsDB


# class SaveTranslationHandler:
#     def __init__(self):
#         self.translations_db = TranslationsDB()

#     def save_translated_lyrics(self, artist_name: str, song_name: str, translated_lyrics: str):
#         """
#         번역된 가사를 데이터베이스에 삽입합니다.

#         Parameters:
#         - artist_name: 아티스트 이름
#         - song_name: 곡 이름
#         - translated_lyrics: 번역된 가사

#         Returns:
#         - 성공 메시지 (str)
#         """
#         try:
#             song_id = self.translations_db.get_song_id(artist_name, song_name)
#             if not song_id:
#                 return f"'{artist_name}'의 '{song_name}' 정보가 데이터베이스에 없습니다. 먼저 곡 정보를 저장해주세요."

#             self.translations_db.insert_translation(song_id, translated_lyrics)
#             return f"'{artist_name}'의 '{song_name}' 번역된 가사가 성공적으로 삽입되었습니다."
#         except Exception as e:
#             print(f"번역된 가사를 삽입하는 중 오류 발생: {e}")
#             return f"'{artist_name}'의 '{song_name}' 번역된 가사 삽입에 실패했습니다."
