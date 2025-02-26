import time
import base64
import httpx
from config_loader import load_config

class SpotifyAPI:
    def __init__(self):
        """Spotify API 초기화 및 토큰 관리"""
        config = load_config()
        self.client_id = config.get('SPOTIFY_CLIENT_ID')
        self.client_secret = config.get('SPOTIFY_CLIENT_SECRET')
        self.base_url = "https://api.spotify.com/v1"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.access_token = None
        self.token_expiry_time = 0  # 토큰 만료 시간을 저장 (유닉스 타임스탬프)

    async def authenticate(self):
        """Spotify API 인증 토큰을 요청하는 메서드"""
        # 기존 토큰이 아직 유효하면 새로 요청할 필요가 없습니다.
        if self.access_token and time.time() < self.token_expiry_time:
            return

        # Base64 인코딩
        auth_str = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(auth_str.encode('utf-8')).decode('ascii')

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {"grant_type": "client_credentials"}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, headers=headers, data=payload)
            response.raise_for_status()
            token_response = response.json()
            self.access_token = token_response.get('access_token')
            expires_in = token_response.get('expires_in')  # 토큰의 유효 기간 (초)
            self.token_expiry_time = time.time() + expires_in  # 만료 시점 계산

    async def get(self, endpoint, params=None):
        """비동기 GET 요청을 처리하는 메서드"""
        # 토큰 갱신이 필요한 경우 먼저 인증
        await self.authenticate()

        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def search(self, query, search_type="artist"):
        """
        Spotify 검색 API를 사용하는 메서드
        - query: 검색할 키워드 (string)
        - search_type: 검색 타입 (기본값: artist, 가능한 값: artist, album, track 등)
        """
        endpoint = "search"
        params = {
            "q": query,
            "type": search_type,
            "limit": 10
        }
        return await self.get(endpoint, params)
    
    async def get_artist_info(self, artist_id):
        """
        Spotify API에서 아티스트 정보를 가져오는 메서드
        - artist_id: Spotify에서 조회할 아티스트의 ID (string)
        """
        endpoint = f"artists/{artist_id}"
        artist_data = await self.get(endpoint)

        if not artist_data:
            return None

        # ✅ 불필요한 `external_urls.spotify` 와 `uri` 필드는 제외하고 반환
        return {
            "artist_id": artist_data.get("id"),
            "artist_name": artist_data.get("name"),
            "followers": artist_data.get("followers", {}).get("total", 0),
            "genres": artist_data.get("genres", []),
            "images": artist_data.get("images", []),  # 여러 해상도의 이미지 리스트
            "popularity": artist_data.get("popularity")
        }
