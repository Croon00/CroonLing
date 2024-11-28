import discord
from discord.ext import commands
from database.db_manager import DBManager
from config_loader import load_config
from apis.translate_chatgpt_api import Translator

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class TranslateLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()
        self.translator = Translator()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='번역')
        async def translate_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 데이터베이스에서 가사를 조회하고 번역"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!번역 Aimer, Torches")
                return

            # 데이터베이스에서 가사 조회
            try:
                lyrics, translated_lyrics, phonetics_lyrics, korean = self.db_manager.get_lyrics(artist, song)

                if lyrics:
                    if not translated_lyrics:
                        # 번역이 없는 경우 API 호출
                        translated_lyrics = self.translator.request(lyrics, request_type="translate")
                        if "오류가 발생했습니다" not in translated_lyrics:
                            # 번역 결과를 DB에 저장
                            self.db_manager.update_translation(artist, song, translated_lyrics)
                        else:
                            await ctx.send("가사 번역 중 오류가 발생했습니다.")
                            return

                    # 번역 결과를 Embed로 출력
                    embed = discord.Embed(
                        title=f"{artist} - {song} 번역된 가사",
                        description=translated_lyrics,
                        color=discord.Color.blue()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
            except Exception as e:
                await ctx.send(f"데이터베이스에서 가사를 조회하거나 번역하는 중 오류가 발생했습니다: {str(e)}")
