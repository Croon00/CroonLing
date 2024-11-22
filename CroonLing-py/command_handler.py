from commands import SearchArtistCommand, GetLyricsCommand
class CommandHandler:
    def __init__(self, bot, genius_api, genius_crawler, translator):
        self.bot = bot

        # 명령어 인스턴스 생성 및 등록
        self.search_artist_command = SearchArtistCommand(bot, genius_api)
        self.search_artist_command.register()

        self.get_lyrics_command = GetLyricsCommand(bot, genius_api, genius_crawler, translator)
        self.get_lyrics_command.register()

