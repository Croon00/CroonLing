from pydantic import BaseModel, Field
from typing import Optional, List
from database.mongodb import mongo_db  # MongoDB 연결 설정 가져오기

# ✅ 아티스트 모델 (artists 컬렉션)
class ArtistModel(BaseModel):
    artist_id: str = Field(..., description="Spotify Artist ID")
    artist_name: str = Field(..., description="Artist Name")
    artist_kr: List[str] = Field(default=[], description="List of Korean Names")

    @staticmethod
    def get_collection():
        return mongo_db["artists"]

# ✅ 곡 모델 (songs 컬렉션)
class SongModel(BaseModel):
    song_id: str = Field(..., description="Spotify Song ID")
    song_name: str = Field(..., description="Song Name")
    artist_id: str = Field(..., description="Reference to Artist ID")
    artist_name: str = Field(..., description="Artist Name")
    artist_kr: List[str] = Field(default=[], description="List of Korean Names")
    korean_song_names: List[str] = Field(default=[], description="List of Korean Song Names")
    album_name: Optional[str] = Field(None, description="Album Name")
    release_date: Optional[str] = Field(None, description="Release Date")
    track_image_url: Optional[str] = Field(None, description="Track Image URL")
    url: Optional[str] = Field(None, description="Spotify URL")
    lyrics: Optional[str] = Field(None, description="Lyrics of the song")
    translated_lyrics: Optional[str] = Field(None, description="Translated lyrics")
    phonetics_lyrics: Optional[str] = Field(None, description="Phonetic representation of lyrics")
    phonetics_korean_lyrics: Optional[str] = Field(None, description="Korean phonetic representation")

    @staticmethod
    def get_collection():
        return mongo_db["songs"]
