# -*- coding: utf-8 -*-
import openai
import json
from apis import APIInterface
from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class ChatgptApi(APIInterface):
    def __init__(self):
        self.client = openai.OpenAI(api_key=config['OPEN_API_TOKEN'])  # ✅ 최신 방식으로 변경

    def request(self, text, request_type="translate"):
        """
        APIInterface의 request 메서드를 구현하여 번역 또는 발음 변환 요청 수행
        - text: 번역할 가사 (string)
        - request_type: 요청 타입 ("translate", "phonetics", "roman_to_korean")
        """
        if request_type == "translate":
            return self.translate(text)
        elif request_type == "phonetics":
            return self.phonetics(text)
        elif request_type == "roman_to_korean":
            return self.roman_to_korean(text)
        else:
            raise ValueError("Invalid request type. Use 'translate', 'phonetics', or 'roman_to_korean'.")

    def translate(self, text):
        """가사를 한국어로 번역하는 메서드"""
        print("번역 api 시작")
        prompt = f"다음 가사를 한국어로 번역해 주세요:\n{text}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": prompt},
                ],
                timeout=60  # 10초 제한 (필요시 조정 가능)
            )

            print("✅ API 응답 받음")  # API 응답 정상 확인
            return response.choices[0].message.content

        except openai.AuthenticationError:
            print("❌ API 키 인증 오류: 키가 올바르지 않거나 만료됨")
        except openai.RateLimitError:
            print("⚠️ 요청 제한 초과 (Rate Limit)")
        except openai.OpenAIError as e:
            print(f"🚨 기타 OpenAI API 오류: {e}")
        except Exception as e:
            print(f"❗ 예상치 못한 오류 발생: {e}")

        return None

    def phonetics(self, text):
        """가사의 발음(로마자)을 변환하는 메서드"""
        prompt = f"다음 가사를 로마자 발음으로 변환해 주세요:\n{text}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"발음 변환 요청 중 오류가 발생했습니다: {str(e)}"

    def roman_to_korean(self, text):
        """로마자 발음을 보고 한국어 발음으로 변환하는 메서드"""
        prompt = f"다음 로마자 발음을 한국어 한글 발음으로 변환해 주세요:\n{text}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator who converts Romanized Japanese text into Korean phonetics."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"로마자 발음 변환 요청 중 오류가 발생했습니다: {str(e)}"
        
        
    def extract_kanji_info(self, text):
        """가사에서 한자를 추출하고, 해당 한자의 뜻, 발음(히라가나), 한국식 한자음, 동사/합성어 여부, JLPT 급수, 예문을 반환"""
        kanji_list = list(set(re.findall(r'[\u4E00-\u9FFF]+', text)))  # 연속된 한자 추출

        if not kanji_list:
            return "해당 가사에서 한자를 찾을 수 없습니다."

        prompt = f"""
        다음 한자 또는 한자 합성어에 대한 정보를 제공해 주세요:
        - 일본어 발음(히라가나)
        - 한국어 뜻
        - 한국식 한자음(훈음/음독)
        - 동사인지 명사인지 구분 후 설명
        - 합성어인 경우 각 한자의 뜻과 합성어 전체 의미 설명
        - JLPT 급수
        - 예문 하나 제공 (일본어+한국어 번역 포함)

        한자 리스트: {', '.join(kanji_list)}

        예시:
        - 漢字 (かんじ) : 한자 (명사)
            - 漢(かん, 한): 중국
            - 字(じ, 자): 글자
            - JLPT N5
            - 예문: 漢字を勉強しています。(한자를 공부하고 있습니다.)
        - 食べる (たべる) : 먹다 (동사)
            - 食(た, 식): 먹다
            - JLPT N5
            - 예문: 毎朝パンを食べます。(매일 아침 빵을 먹습니다.)
        - 友達 (ともだち) : 친구 (명사)
            - 友(とも, 우): 벗
            - 達(たち, 달): 복수 표현
            - JLPT N5
            - 예문: 友達と遊びます。(친구와 놉니다.)
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a language expert providing detailed kanji explanations."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"한자 정보 요청 중 오류가 발생했습니다: {str(e)}"
