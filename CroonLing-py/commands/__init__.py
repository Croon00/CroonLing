from .search_artist import SearchArtistCommand
from .get_lyrics import GetLyricsCommand
from .get_lyrics_google import GetGoogleLyricsCommand
from .phonetics_lyrics import PhoneticsLyricsCommand
from .translate_lyrics import TranslateLyricsCommands
from .phonetics_korean import GetKoreanLyricsCommand
from .get_artist_songs_albums import GetSpotifyArtistAlbumsCommands
from .get_artist_songs_single import GetSpotifySinglesCommands
from .get_artist_songs_total import GetSpotifyAllTracksCommands

__all__ = [
    "SearchArtistCommand",
    "GetLyricsCommand",
    "GetGoogleLyricsCommand",
    "PhoneticsLyricsCommand",
    "TranslateLyricsCommands",
    "GetKoreanLyricsCommand",
    "GetArtistSongsCommand",
    "GetSpotifyArtistAlbumsCommands",
    "GetSpotifySinglesCommands",
    "GetSpotifyAllTracksCommands",
    "GetSpotifyArtistCommands",
]
