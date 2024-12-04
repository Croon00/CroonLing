import requests
from bs4 import BeautifulSoup

def scrape_lyrics(song_url):
    """
    주어진 노래 URL에서 가사를 스크래핑하여 반환합니다.

    :param song_url: 가사를 가져올 노래의 Genius 페이지 URL
    :return: 가사 문자열 또는 None (가사를 찾지 못한 경우)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(song_url, headers=headers)

    if response.status_code != 200:
        print(f"페이지를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 가사 컨테이너 찾기
    lyrics_container = soup.find('div', {'data-lyrics-container': 'true'})
    if not lyrics_container:
        print("가사 컨테이너를 찾을 수 없습니다.")
        return None

    # 가사 추출
    lyrics = []
    for line in lyrics_container.find_all(['p', 'br']):
        if line.name == 'br':
            lyrics.append('\n')
        else:
            lyrics.append(line.get_text())

    return ''.join(lyrics).strip()
