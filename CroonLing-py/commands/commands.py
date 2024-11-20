from discord.ext import commands
import discord

class CommandHandler:
    def __init__(self, bot, genius_api=None, genius_crawler=None, translator=None):
        self.bot = bot
        self.genius_api = genius_api
        self.genius_crawler = genius_crawler
        self.translator = translator

        # 명령어 등록
        self.bot.add_command(self.search_artist)
        self.bot.add_command(self.get_lyrics)  # get_lyrics 명령어도 등록

    @commands.command(name='가수')
    async def search_artist(self, ctx, *, artist_name: str):
        """가수 이름을 입력받아 Genius API에서 검색합니다."""
        if self.genius_api:
            result = await self.genius_api.search_song(artist_name)
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
                            value=(f"**ID:** {song_id}\n"
                                   f"**Lyrics Owner ID:** {lyrics_owner_id}\n"
                                   f"**Lyrics State:** {lyrics_state}"),
                            inline=False
                        )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"'{artist_name}'의 곡을 찾을 수 없습니다.")
            else:
                await ctx.send("검색 중 오류가 발생했습니다.")
        else:
            await ctx.send("Genius API 인스턴스가 없습니다.")

    @commands.command(name='가사')
    async def get_lyrics(self, ctx, artist: str, *, song: str):
        """가수와 곡 제목을 입력받아 가사 번역"""
        if self.genius_api and self.genius_crawler and self.translator:
            try:
                # Genius API를 이용해 가수 이름으로 검색
                search_result = await self.genius_api.search(artist)  # artist만 검색
                if search_result and 'response' in search_result and 'hits' in search_result['response']:
                    hits = search_result['response']['hits']

                    # 입력된 곡 제목과 일치하는 항목 찾기
                    matching_song = next(
                    (hit for hit in hits if song.lower() in hit['result']['title'].lower()),
                        None
                    )

                    if matching_song:
                        song_url = matching_song['result']['url']

                        # GeniusCrawler로 가사 크롤링
                        self.genius_crawler.start_browser()
                        lyrics = self.genius_crawler.fetch_lyrics(song_url)
                        self.genius_crawler.close_browser()

                        if not lyrics:
                            await ctx.send(f"'{artist} - {song}'의 가사를 찾을 수 없습니다.")
                            return

                        # Translator를 이용해 번역
                        translation_result = self.translator.translate_and_phonetics(lyrics)

                        # 번역 결과를 Discord Embed로 전송
                        embed = discord.Embed(
                            title=f"{artist} - {song} 번역 결과",
                            description=f"[원본 가사 보기]({song_url})",
                            color=discord.Color.green()
                        )
                        embed.add_field(name="번역", value=translation_result["translation"], inline=False)
                        embed.add_field(name="발음", value=translation_result["phonetics"], inline=False)

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"'{artist} - {song}'에 대한 정확한 결과를 찾을 수 없습니다.")
                else:
                    await ctx.send("검색 중 오류가 발생했습니다.")
            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
        else:
            await ctx.send("필요한 API 인스턴스가 초기화되지 않았습니다.")

