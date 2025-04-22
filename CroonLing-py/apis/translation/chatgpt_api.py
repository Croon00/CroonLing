# -*- coding: utf-8 -*-
import openai
import json
import logging
import re
from apis import APIInterface
from config_loader import load_config

# 환경 변수에서 API 키 불러오기
config = load_config()

class ChatgptApi(APIInterface):
    def __init__(self):
        self.client = openai.OpenAI(api_key=config['OPEN_API_TOKEN'])

    async def request(self, text, request_type="translate"):
        if request_type == "translate":
            return await self.translate(text)
        elif request_type == "phonetics":
            return await self.phonetics(text)
        elif request_type == "roman_to_korean":
            return await self.roman_to_korean(text)
        else:
            raise ValueError("Invalid request type.")

    async def translate(self, text):
        prompt = f"다음 가사를 한국어로 번역해 주세요:\n{text}"
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": prompt},
                ],
                timeout=60
            )
            return response.choices[0].message.content
        except openai.AuthenticationError:
            logging.error("❌ API 키 인증 오류")
        except openai.RateLimitError:
            logging.warning("⚠️ 요청 제한 초과")
        except openai.OpenAIError as e:
            logging.error(f"🚨 OpenAI 오류: {e}")
        except Exception as e:
            logging.error(f"❗ 기타 오류: {e}")
        return None

    async def phonetics(self, text):
        prompt = f"다음 가사를 로마자 발음으로 변환해 주세요:\n{text}"
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": prompt},
                ]
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            logging.error(f"🚨 발음 변환 오류: {e}")
            return f"발음 변환 요청 중 오류가 발생했습니다: {str(e)}"

    async def roman_to_korean(self, text):
        prompt = f"다음 로마자 발음을 한국어 한글 발음으로 변환해 주세요:\n{text}"
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful translator who converts Romanized Japanese text into Korean phonetics."},
                    {"role": "user", "content": prompt},
                ]
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            logging.error(f"🚨 한글 발음 변환 오류: {e}")
            return f"로마자 발음 변환 요청 중 오류가 발생했습니다: {str(e)}"

    async def extract_kanji_info(self, text):
        try:
            logging.info(f"🔍 원본 텍스트 길이: {len(text)}")

            kanji_kana_list = list(set(re.findall(r'[\u4E00-\u9FFF]+[\u3040-\u309F]*', text)))
            logging.info(f"🈶 추출된 한자+히라가나 개수: {len(kanji_kana_list)} | 목록: {kanji_kana_list}")

            if not kanji_kana_list:
                logging.warning("❌ 한자가 포함되지 않음")
                return "해당 가사에서 한자를 찾을 수 없습니다."

            prompt = f"""
            가사에서 **N3 이상의 한자(한자+히라가나 포함)**를 찾아 한 줄 요약으로 제공해 주세요.  
            각 단어의 **일본어 발음, 한국어 뜻, 음독·훈독, 품사(명사/형용사/동사)** 정보를 짧게 정리하세요.  

            📌 예시
            - 経験 (けいけん, 경험, 명사) 経(けい/へ, 경: 지나다) 験(けん/ため, 험: 시험)
            - 積む (つむ, 쌓다, 동사) 積(せき/つ, 적: 쌓다)

            🎵 한자 리스트: {', '.join(kanji_kana_list)}
            """

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a language expert providing detailed kanji explanations."},
                    {"role": "user", "content": prompt},
                ]
            )
            result = response.choices[0].message.content
            logging.info("✅ 한자 정보 추출 완료")
            return result

        except openai.AuthenticationError:
            logging.error("❌ API 키 인증 오류")
            return "API 키 오류 발생. 관리자에게 문의하세요."
        except openai.RateLimitError:
            logging.warning("⚠️ 요청 제한 초과")
            return "현재 요청이 많아 잠시 후 다시 시도해주세요."
        except openai.OpenAIError as e:
            logging.error(f"🚨 OpenAI 오류: {e}")
            return f"OpenAI API 오류 발생: {str(e)}"
        except Exception as e:
            logging.error(f"❗ 예기치 못한 오류: {e}")
            return f"오류가 발생했습니다: {str(e)}"
