import httpx
import json
import asyncio

class GeniusAPI:
    def __init__(self, config_file="config.json"):
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.load_token(config_file)}"}
        
    def load_token(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
            return config["GENUS_API_TOKEN"]
        
    async def get(self, endpoint, params=None):
        """비동기 GET 요청을 처리하는 메서드"""
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def search_song(self, artist_name):
        """특정 아티스트의 노래를 검색하는 비동기 메서드"""
        endpoint = "search"
        params = {"q": artist_name}
        return await self.get(endpoint, params)



