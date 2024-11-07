from discord.ext import commands
from apis.genius_api import GeniusAPI
import discord

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
                # Discord Embed 객체 생성
                embed = discord.Embed(title=f"가수 '{artist_name}'의 곡 목록", color=discord.Color.blue())
                for hit in songs:
                    title = hit['result']['title']
                    song_id = hit['result']['id']
                    lyrics_owner_id = hit['result']['lyrics_owner_id']
                    lyrics_state = hit['result']['lyrics_state']

                    # 곡별로 Embed에 추가
                    embed.add_field(
                        name=title,
                        value=(
                            f"**ID:** {song_id}\n"
                            f"**Lyrics Owner ID:** {lyrics_owner_id}\n"
                            f"**Lyrics State:** {lyrics_state}"
                        ),
                        inline=False
                    )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"'{artist_name}'의 곡을 찾을 수 없습니다.")
        else:
            await ctx.send("검색 중 오류가 발생했습니다.")
