import requests
import json

class GeniusAPI:
    def __init__(self, config_file="config.json"):
        self.base_url = "https://api.genius.com"  # 오타 수정
        self.headers = {"Authorization": f"Bearer {self.load_token(config_file)}"}
        
    def load_token(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
            return config["GENUS_API_TOKEN"]
        
    def get(self, endpoint, params=None):
        """GET 요청을 처리하는 메서드"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴
        return response.json()
    
    def search_song(self, artist_name):
        """특정 아티스트의 노래를 검색하는 메서드"""
        endpoint = "search"
        params = {"q": artist_name}
        return self.get(endpoint, params)


