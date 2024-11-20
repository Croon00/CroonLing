import httpx
import json

class GeniusAPI:
    def __init__(self, api_token):
        """Genius API 초기화"""
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

    async def search(self, artist_name):
        """
        특정 아티스트의 노래를 검색하는 메서드
        - artist_name: 검색할 아티스트 이름 (string)
        """
        endpoint = "search"
        params = {"q": artist_name}
        return await self.get(endpoint, params)
    
    async def get_song_by_id(self, song_id):
        """
        특정 곡의 상세 정보를 가져오는 메서드
        - song_id: 곡 ID (int)
        """
        endpoint = f"songs/{song_id}"  # 엔드포인트에 곡 ID 포함
        return await self.get(endpoint)
