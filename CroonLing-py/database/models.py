from pydantic import BaseModel, Field
from typing import Optional, List
from database.mongodb import mongo_db  # MongoDB 연결 설정 가져오기

# ✅ 아티스트 모델 (artists 컬렉션)
class ArtistModel(BaseModel):
    artist_id: str = Field(..., description="Spotify Artist ID")
    artist_names: List[str] = Field(default=[], description="List of Artist Names (English, Korean, etc.)")
    genres: List[str] = Field(default=[], description="List of artist's music genres")
    popularity: Optional[int] = Field(None, description="Popularity score (0-100)")
    followers: Optional[int] = Field(None, description="Number of followers on Spotify")
    profile_image_url: Optional[str] = Field(None, description="URL of the artist's profile image")
    external_url: Optional[str] = Field(None, description="Spotify artist profile URL")

    @staticmethod
    def get_collection():
        return mongo_db["artists"]

# ✅ 곡 모델 (songs 컬렉션) — 가사 관련 필드 제거됨
class SongModel(BaseModel):
    song_id: str = Field(..., description="Spotify Song ID")
    song_names: List[str] = Field(default=[], description="List of Song Names (English, Korean, etc.)")
    artist_id: str = Field(..., description="Reference to Artist ID")
    artist_names: List[str] = Field(default=[], description="List of Artist Names (English, Korean, etc.)")
    album_name: Optional[str] = Field(None, description="Album Name")
    release_date: Optional[str] = Field(None, description="Release Date")
    track_image_url: Optional[str] = Field(None, description="Track Image URL")
    url: Optional[str] = Field(None, description="Spotify URL")

    @staticmethod
    def get_collection():
        return mongo_db["songs"]

# ✅ 필요 시, lyrics 모델도 따로 만들 수 있음
class LyricsModel(BaseModel):
    song_id: str = Field(..., description="참조할 Song ID")
    lyrics: Optional[str] = None
    translated_lyrics: Optional[str] = None
    phonetics_lyrics: Optional[str] = None
    phonetics_korean_lyrics: Optional[str] = None
    kanji_info: Optional[str] = None

    @staticmethod
    def get_collection():
        return mongo_db["lyrics"]
