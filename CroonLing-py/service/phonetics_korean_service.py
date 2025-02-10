from database import PhoneticsKoreanDB
from service import PhoneticsService
from apis import Translator

class PhoneticsKoreanService:
    def __init__(self):
        self.phonetics_korean_db = PhoneticsKoreanDB()
        self.phonetics_service = PhoneticsService()  # 로마자 발음 조회를 위해 추가
        self.translator = Translator()

    def get_korean_phonetics(self, song_id):
        """
        곡의 한글 발음 가져오기
        """
        korean_phonetics = self.phonetics_korean_db.find_phonetics_korean(song_id)
        return korean_phonetics if korean_phonetics else None

    def generate_and_save_korean_phonetics(self, song_id):
        """
        곡의 로마자 발음을 기반으로 한글 발음을 생성하고 DB에 저장
        """
        # 로마자 발음 가져오기
        roman_pronunciation = self.phonetics_service.get_phonetics(song_id)
        if not roman_pronunciation:
            return None  # 로마자 발음이 없으면 변환 불가

        # 한국어 발음 변환
        korean_pronunciation = self.translator.roman_to_korean(roman_pronunciation)
        if not korean_pronunciation or "오류" in korean_pronunciation:
            return None  # 변환 실패

        # DB에 저장
        self.phonetics_korean_db.upsert_phonetics_korean(song_id, korean_pronunciation)
        return korean_pronunciation

    def save_korean_phonetics(self, song_id: str, korean_phonetics_lyrics: str):
        """
        한국어 발음을 데이터베이스에 삽입 또는 업데이트
        """
        try:
            self.phonetics_korean_db.upsert_phonetics_korean(song_id, korean_phonetics_lyrics)
            return f"곡 ID '{song_id}'의 한국어 발음이 성공적으로 업데이트되었습니다."
        except Exception as e:
            print(f"한국어 발음을 업데이트하는 중 오류 발생: {e}")
            return f"곡 ID '{song_id}'의 한국어 발음 업데이트에 실패했습니다."
