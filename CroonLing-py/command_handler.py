from commands import (
    AddArtistNameKr,
    AddSongNameKr,
    FetchArtistSongsAlbums,
    FetchArtistSongsSingle,
    FetchArtistSongsTotal,
    FetchSingleSong
)

class CommandHandler:
    def __init__(self, bot, genius_api, genius_crawler, translator):
        self.bot = bot

        # 명령어 인스턴스 생성 및 등록
        self.phonetics_lyrics_command = AddArtistNameKr(bot)
        self.phonetics_lyrics_command.register()

        self.translate_lyrics_command = AddSongNameKr(bot)
        self.translate_lyrics_command.register()

        self.get_korean_lyrics_command = FetchArtistSongsAlbums(bot)
        self.get_korean_lyrics_command.register()

        self.get_spotify_all_tracks_command = FetchArtistSongsSingle(bot)
        self.get_spotify_all_tracks_command.register()

        self.get_spotify_artist_albums_command = FetchArtistSongsTotal(bot)
        self.get_spotify_artist_albums_command.register()

        self.get_spotify_singles_command = FetchSingleSong(bot)
        self.get_spotify_singles_command.register()

