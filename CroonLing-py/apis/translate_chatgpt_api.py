import openai
import json


class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def translate_and_phonetics(self, text):
        # ChatGPT에게 요청할 Prompt 생성
        prompt = f"""
        아래 일본어 가사를 한국어로 번역하고, 각 줄에 일본어 발음(로마자 발음도 가능)을 추가해 주세요.
        가사:
        {text}

        출력 형식:
        {{
            "translation": "번역된 가사",
            "phonetics": "발음 변환된 가사"
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt},
            ],
        )
        result = response['choices'][0]['message']['content']
        return json.loads(result)

    def save_to_file(self, data, output_file="output.json"):
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Translation saved to {output_file}")
