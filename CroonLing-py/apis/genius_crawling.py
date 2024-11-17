import requests
from bs4 import BeautifulSoup

# 사이트 요청
url = "https://genius.com/Aimer-800-lyrics"
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')

# data-lyrics-container 속성을 가진 div 요소 찾기
lyrics_container = soup.find('div', {'data-lyrics-container': 'true'})


# 가사 내용 추출 및 줄바꿈 처리
lyrics = []
for element in lyrics_container.find_all(['br', 'div'], recursive=False):
    if element.name == 'br':
        lyrics.append("\n")  # <br> 태그를 줄바꿈으로 처리
    elif element.name == 'div':
        print("가나")
        lyrics.append(element.get_text(strip=True))  # 텍스트 추출

# 가사 출력
cleaned_lyrics = "".join(lyrics).strip()

print(cleaned_lyrics)
