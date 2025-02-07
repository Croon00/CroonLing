from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import mongo_db  # MongoDB 연결 설정 가져오기

# ✅ 아티스트 모델 (artists 컬렉션)
class ArtistModel(BaseModel):
    artist_id: str = Field(..., description="Spotify Artist ID")
    artist_name: str = Field(..., description="Artist Name")

    @staticmethod
    def get_collection():
        return mongo_db["artists"]

# ✅ 곡 모델 (songs 컬렉션)
class SongModel(BaseModel):
    song_id: str = Field(..., description="Spotify Song ID")
    song_name: str = Field(..., description="Song Name")
    artist_id: str = Field(..., description="Reference to Artist ID")
    artist_name: str = Field(..., description="Artist Name")
    album_name: Optional[str] = Field(None, description="Album Name")
    release_date: Optional[str] = Field(None, description="Release Date")
    track_image_url: Optional[str] = Field(None, description="Track Image URL")
    url: Optional[str] = Field(None, description="Spotify URL")

    @staticmethod
    def get_collection():
        return mongo_db["songs"]

# ✅ 한국어 아티스트 이름 모델 (artist_kr 컬렉션)
class ArtistKRModel(BaseModel):
    artist_id: str = Field(..., description="Reference to Artist ID")
    artist_kr_name: str = Field(..., description="Korean Name of the Artist")

    @staticmethod
    def get_collection():
        return mongo_db["artist_kr"]

# ✅ 가사 모델 (lyrics 컬렉션)
class LyricsModel(BaseModel):
    song_id: str = Field(..., description="Reference to Song ID")
    lyrics: str = Field(..., description="Lyrics of the song")

    @staticmethod
    def get_collection():
        return mongo_db["lyrics"]

# ✅ 번역된 가사 모델 (translations 컬렉션)
class TranslationsModel(BaseModel):
    song_id: str = Field(..., description="Reference to Song ID")
    translated_lyrics: str = Field(..., description="Translated lyrics")

    @staticmethod
    def get_collection():
        return mongo_db["translations"]

# ✅ 발음 데이터 모델 (phonetics 컬렉션)
class PhoneticsModel(BaseModel):
    song_id: str = Field(..., description="Reference to Song ID")
    phonetics_lyrics: Optional[str] = Field(None, description="Phonetic representation of lyrics")
    korean_phonetics_lyrics: Optional[str] = Field(None, description="Korean phonetic representation")

    @staticmethod
    def get_collection():
        return mongo_db["phonetics"]

# ✅ 한국어 발음 데이터 모델 (korean_phonetics 컬렉션)
class PhoneticsKoreanModel(BaseModel):
    song_id: str = Field(..., description="Reference to Song ID")
    phonetics_korean_lyrics: str = Field(..., description="Korean phonetic representation")

    @staticmethod
    def get_collection():
        return mongo_db["phonetics_korean"]