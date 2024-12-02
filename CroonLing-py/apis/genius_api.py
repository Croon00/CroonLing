import httpx
from .api_interface import APIInterface
from config_loader import load_config

class GeniusAPI(APIInterface):
    def __init__(self):
        """Genius API 초기화"""
        config = load_config()
        api_token = config.get('GENIUS_API_TOKEN')
        if not api_token:
            raise ValueError("GENIUS_API_TOKEN이 config.json에 설정되어 있지 않습니다.")
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    async def get(self, endpoint, params=None):
        """
        비동기 GET 요청을 처리하는 메서드
        - endpoint: 요청할 엔드포인트 (e.g., "search")
        - params: 추가 GET 파라미터 (dict 형태)
        """
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            return response.json()

    async def request(self, endpoint, params=None):
        """
        APIInterface의 request 메서드를 구현
        """
        return await self.get(endpoint, params)

    async def search(self, artist_name):
        """
        특정 아티스트의 노래를 검색하는 메서드
        - artist_name: 검색할 아티스트 이름 (string)
        """
        endpoint = "search"
        params = {"q": artist_name}
        return await self.request(endpoint, params)

    async def get_song_by_id(self, song_id):
        """
        특정 곡의 상세 정보를 가져오는 메서드
        - song_id: 곡 ID (int)
        """
        endpoint = f"songs/{song_id}"
        return await self.request(endpoint)

    async def get_artist_songs(self, artist_id, per_page=50):
        """
        특정 아티스트의 모든 곡 제목을 가져오는 메서드
        - artist_id: 아티스트 ID (int)
        - per_page: 한 페이지당 가져올 곡 수 (기본값: 50)
        """
        songs = []
        page = 1
        while True:
            endpoint = f"artists/{artist_id}/songs"
            params = {
                "per_page": per_page,
                "page": page,
                "sort": "title"  # 제목 순으로 정렬
            }
            data = await self.request(endpoint, params)
            page_songs = data['response']['songs']
            if not page_songs:
                break
            songs.extend(page_songs)
            page += 1
        return [song['title'] for song in songs]
