from discord.ext import commands
from api.genius_api import GeniusAPI

class CommandHandler:
    def __init__(self, bot, genius_api):
        self.bot = bot
        self.genius_api = genius_api

        # 명령어 등록
        self.bot.add_command(self.search_artist)

    @commands.command(name='가수')
    async def search_artist(self, ctx, *, artist_name: str):
        """가수 이름을 입력받아 Genius API에서 검색합니다."""
        result = self.genius_api.search_song(artist_name)
        if result and 'response' in result and 'hits' in result['response']:
            songs = result['response']['hits']
            if songs:
                song_titles = [hit['result']['title'] for hit in songs]
                await ctx.send(f"가수 '{artist_name}'의 곡: {', '.join(song_titles)}")
            else:
                await ctx.send(f"'{artist_name}'의 곡을 찾을 수 없습니다.")
        else:
            await ctx.send("검색 중 오류가 발생했습니다.")


