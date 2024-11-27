import discord
from discord.ext import commands
from database.db_manager import DBManager
from config_loader import load_config
from apis.translate_chatgpt_api import Translator

class PhoneticsLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager(config)
        self.translator = Translator(api_key=config['openai_api_key'])

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='발음')
        async def phonetics_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 데이터베이스에서 가사를 조회하고 발음 변환"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!발음 Aimer, Torches")
                return

            # 데이터베이스에서 가사 조회
            try:
                lyrics, _, phonetics_lyrics = self.db_manager.get_lyrics(artist, song)
                if lyrics:
                    # 가사 발음 변환이 이미 있는 경우 사용
                    if not phonetics_lyrics:
                        # 가사 발음 변환 요청
                        phonetics_lyrics = self.translator.request(lyrics, request_type="phonetics")
                        self.db_manager.update_phonetics(artist, song, phonetics_lyrics)
                    embed = discord.Embed(
                        title=f"{artist} - {song} 발음 변환된 가사",
                        description=phonetics_lyrics,
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
            except Exception as e:
                await ctx.send(f"데이터베이스에서 가사를 조회하거나 발음 변환하는 중 오류가 발생했습니다: {str(e)}")