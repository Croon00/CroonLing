import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def load_config():
    """환경 변수에서 모든 설정 값 로드"""
    return {
        "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
        "GENIUS_API_TOKEN": os.getenv("GENIUS_API_TOKEN"),
        "OPEN_API_TOKEN": os.getenv("OPEN_API_TOKEN"),
        "MONGO_URI": os.getenv("MONGO_URI"),
        "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
        "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "KAFKA_BOOTSTRAP_SERVERS": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "SERPAPI_KEY": os.getenv("SERPAPI_KEY"),
        "GCP_CRAWLER_IP": os.getenv("GCP_CRAWLER_IP"),
        "GCP_CRAWLER_PORT": os.getenv("GCP_CRAWLER_PORT")
    }