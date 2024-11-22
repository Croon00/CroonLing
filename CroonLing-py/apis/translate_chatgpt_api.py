# -*- coding: utf-8 -*-
import openai
import json
from .api_interface import APIInterface

class Translator(APIInterface):
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def request(self, text, request_type="translate"):
        """
        APIInterface의 request 메서드를 구현하여 번역 또는 발음 변환 요청 수행
        - text: 번역할 가사 (string)
        - request_type: 요청 타입 ("translate" 또는 "phonetics")
        """
        if request_type == "translate":
            return self.translate(text)
        elif request_type == "phonetics":
            return self.phonetics(text)
        else:
            raise ValueError("Invalid request type. Use 'translate' or 'phonetics'.")

    def translate(self, text):
        """
        일본어 가사를 한국어로 번역하는 메서드
        - text: 번역할 가사 (string)
        """
        prompt = f"아래 일본어 가사를 한국어로 번역해 주세요.\n가사:\n{text}\n번역된 가사:"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt},
            ],
        )
        return response['choices'][0]['message']['content']

    def phonetics(self, text):
        """
        일본어 가사의 발음(로마자)을 변환하여 제공하는 메서드
        - text: 변환할 가사 (string)
        """
        prompt = f"아래 일본어 가사의 발음(로마자 발음)을 추가해 주세요.\n가사:\n{text}\n발음 변환된 가사:"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt},
            ],
        )
        return response['choices'][0]['message']['content']
