from commands import (
    SearchArtistCommand,
    GetGoogleLyricsCommand,
    PhoneticsLyricsCommand,
    TranslateLyricsCommands,
    GetKoreanLyricsCommand,
    GetSpotifyAllTracksCommands,
    GetSpotifyArtistAlbumsCommands,
    GetSpotifySinglesCommands,
)

class CommandHandler:
    def __init__(self, bot, genius_api, genius_crawler, translator):
        self.bot = bot

        # 명령어 인스턴스 생성 및 등록
        self.search_artist_command = SearchArtistCommand(bot, genius_api)
        self.search_artist_command.register()
        
        self.get_google_lyrics_command = GetGoogleLyricsCommand(bot)
        self.get_google_lyrics_command.register()

        self.phonetics_lyrics_command = PhoneticsLyricsCommand(bot)
        self.phonetics_lyrics_command.register()

        self.translate_lyrics_command = TranslateLyricsCommands(bot)
        self.translate_lyrics_command.register()

        self.get_korean_lyrics_command = GetKoreanLyricsCommand(bot)
        self.get_korean_lyrics_command.register()

        self.get_spotify_all_tracks_command = GetSpotifyAllTracksCommands(bot)
        self.get_spotify_all_tracks_command.register()

        self.get_spotify_artist_albums_command = GetSpotifyArtistAlbumsCommands(bot)
        self.get_spotify_artist_albums_command.register()

        self.get_spotify_singles_command = GetSpotifySinglesCommands(bot)
        self.get_spotify_singles_command.register()

