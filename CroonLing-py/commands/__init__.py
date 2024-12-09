from .get_lyrics import GetLyricsCommand
from .phonetics_lyrics import PhoneticsLyricsCommand
from .translate_lyrics import TranslateLyricsCommands
from .phonetics_korean import GetKoreanLyricsCommand
from .get_artist_songs_albums import GetSpotifyArtistAlbumsCommands
from .get_artist_songs_single import GetSpotifySinglesCommands
from .get_artist_songs_total import GetSpotifyAllTracksCommands

__all__ = [
    "GetLyricsCommand",
    "PhoneticsLyricsCommand",
    "TranslateLyricsCommands",
    "GetKoreanLyricsCommand",
    "GetArtistSongsCommand",
    "GetSpotifyArtistAlbumsCommands",
    "GetSpotifySinglesCommands",
    "GetSpotifyAllTracksCommands",
    "GetSpotifyArtistCommands",
]
