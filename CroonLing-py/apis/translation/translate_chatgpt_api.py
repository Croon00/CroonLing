# -*- coding: utf-8 -*-
import openai
import json
from apis import APIInterface
from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class Translator(APIInterface):
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
