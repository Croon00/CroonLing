from discord.ext import commands
import discord
from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class GetLyricsCommand:
    def __init__(self, bot, genius_api, genius_crawler, translator):
        self.bot = bot
        self.genius_api = genius_api
        self.genius_crawler = genius_crawler
        self.translator = translator

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='가사')
        async def get_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 가사 검색"""
            try:
                artist, song = query.split(maxsplit=1)
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!가사 Aimer 800")
                return

            if self.genius_api and self.genius_crawler and self.translator:
                try:
                    # "로딩 중..."을 사용자에게 보여줍니다.
                    async with ctx.typing():
                        # Genius API를 이용해 가수 이름으로 검색
                        search_result = await self.genius_api.search(artist)
                        if search_result and 'response' in search_result and 'hits' in search_result['response']:
                            hits = search_result['response']['hits']

                            # 검색 결과를 통해 일치하는 곡 찾기
                            matching_song = next(
                                (hit for hit in hits if song.lower() in hit['result']['full_title'].lower()), None
                            )
                            if matching_song:
                                song_url = matching_song['result']['url']

                                # GeniusCrawler로 가사 크롤링
                                self.genius_crawler.start_browser()
                                lyrics = self.genius_crawler.request(song_url)
                                self.genius_crawler.close_browser()

                                if not lyrics:
                                    await ctx.send(f"'{artist} - {song}'의 가사를 찾을 수 없습니다.")
                                    return

                                # 가사 결과를 Discord Embed로 전송
                                embed = discord.Embed(
                                    title=f"{artist} - {song} 가사",
                                    description=f"[원본 가사 보기]({song_url})",
                                    color=discord.Color.green()
                                )

                                # 가사를 1024자 이하로 나누어 여러 임베드 필드에 추가
                                for i in range(0, len(lyrics), 1024):
                                    embed.add_field(name="가사", value=lyrics[i:i+1024], inline=False)

                                await ctx.send(embed=embed)
                            else:
                                await ctx.send(f"'{artist} - {song}'에 대한 정확한 결과를 찾을 수 없습니다.")
                        else:
                            await ctx.send("검색 중 오류가 발생했습니다.")
                except Exception as e:
                    await ctx.send(f"오류 발생: {str(e)}")
            else:
                await ctx.send("필요한 API 인스턴스가 초기화되지 않았습니다.")
