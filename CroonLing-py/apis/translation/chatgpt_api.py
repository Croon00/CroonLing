# -*- coding: utf-8 -*-
import openai
import json
from apis import APIInterface
from config_loader import load_config
import logging
import re

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
        """가사에서 한자를 추출하고, 해당 한자의 뜻, 발음(히라가나), 한국식 한자음, 동사/합성어 여부, JLPT 급수 반환"""

        try:
            # ✅ 로그 추가: 원본 텍스트 길이 확인
            logging.info(f"🔍 원본 텍스트 길이: {len(text)}")

            # ✅ 한자 + 히라가나 조합 추출 (동사, 형용사 포함)
            kanji_kana_list = list(set(re.findall(r'[\u4E00-\u9FFF]+[\u3040-\u309F]*', text)))
            logging.info(f"🈶 추출된 한자(히라가나 포함) 개수: {len(kanji_kana_list)} | 목록: {kanji_kana_list}")

            if not kanji_kana_list:
                logging.warning("❌ 한자가 포함되지 않은 텍스트입니다.")
                return "해당 가사에서 한자를 찾을 수 없습니다."

            # ✅ ChatGPT 프롬프트 최적화
            prompt = f"""
            가사에서 **N3 이상의 한자(한자+히라가나 포함)**를 찾아 한 줄 요약으로 제공해 주세요.  
            각 단어의 **일본어 발음, 한국어 뜻, 음독·훈독, 품사(명사/형용사/동사)** 정보를 짧게 정리하세요.  

            📌 **형식 예시**
            - 経験 (けいけん, 경험, 명사) 経(けい/へ, 경: 지나다) 験(けん/ため, 험: 시험)  
            - 積む (つむ, 쌓다, 동사) 積(せき/つ, 적: 쌓다)  
            - 認識する (にんしきする, 인식하다, 동사) 認(にん/みと, 인: 알다) 識(しき/し, 식: 알다)  

            🎵 **가사에서 추출된 한자 리스트:** {', '.join(kanji_kana_list)}
            """

            # ✅ API 요청 및 예외 처리
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "You are a language expert providing detailed kanji explanations."},
                        {"role": "user", "content": prompt},
                    ],
                )
                result = response.choices[0].message.content
                logging.info("✅ API 응답 성공: 한자 정보 추출 완료")
                return result

            except openai.AuthenticationError:
                logging.error("❌ API 키 인증 오류: 키가 올바르지 않거나 만료됨")
                return "API 키 오류 발생. 관리자에게 문의하세요."

            except openai.RateLimitError:
                logging.error("⚠️ OpenAI 요청 제한 초과 (Rate Limit)")
                return "현재 요청이 많아 잠시 후 다시 시도해주세요."

            except openai.OpenAIError as e:
                logging.error(f"🚨 기타 OpenAI API 오류: {e}")
                return f"OpenAI API 오류 발생: {str(e)}"

        except Exception as e:
            logging.error(f"❗ 예상치 못한 오류 발생: {e}")
            return f"오류가 발생했습니다: {str(e)}"
