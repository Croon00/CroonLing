from database import PhoneticsDB
from apis import Translator
from service import LyricsService

class PhoneticsService:
    def __init__(self):
        self.phonetics_db = PhoneticsDB()
        self.translator = Translator()
        self.lyrics_service = LyricsService()  # 가사 조회를 위해 추가

    def get_phonetics(self, song_id):
        """
        곡의 로마자 발음 가져오기
        """
        phonetics_lyrics = self.phonetics_db.find_phonetics(song_id)
        return phonetics_lyrics if phonetics_lyrics else None

    def generate_and_save_phonetics(self, song_id):
        """
        곡의 가사에서 발음을 생성하고 DB에 저장
        """
        # 가사 가져오기
        lyrics = self.lyrics_service.get_lyrics(song_id)
        if not lyrics:
            return None  # 가사가 없으면 발음도 생성 불가

        # 발음 변환
        pronunciation = self.translator.phonetics(lyrics)
        if not pronunciation or "오류" in pronunciation:
            return None  # 변환 실패

        # DB에 저장
        self.phonetics_db.upsert_phonetics(song_id, pronunciation)
        return pronunciation

    def save_phonetics(self, song_id: str, phonetics_lyrics: str):
        """
        로마자 발음을 데이터베이스에 삽입 또는 업데이트
        """
        try:
            self.phonetics_db.upsert_phonetics(song_id, phonetics_lyrics)
            return f"곡 ID '{song_id}'의 로마자 발음이 성공적으로 업데이트되었습니다."
        except Exception as e:
            print(f"로마자 발음을 업데이트하는 중 오류 발생: {e}")
            return f"곡 ID '{song_id}'의 로마자 발음 업데이트에 실패했습니다."
