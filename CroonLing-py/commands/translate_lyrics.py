import discord
from discord.ext import commands
from discord.ui import Button, View
from service.translation_handler import TranslationHandler
from service.lyrics_handler import LyricsHandler


class TranslateLyricsCommands:
    def __init__(self, bot):
        self.bot = bot
        self.translation_handler = TranslationHandler()
        self.lyrics_handler = LyricsHandler()

    def register(self):
        @self.bot.command(name='번역')
        async def translate_lyrics(ctx, *, input_text: str):
            """
            !!번역 (가수이름), (노래제목)
            - 가사 번역 처리 및 DB 저장
            """
            await ctx.send("번역 작업을 시작합니다...")

            try:
                # 입력 형식 검사
                if ',' not in input_text:
                    await ctx.send("올바른 형식으로 입력해주세요. 예: !!번역 Aimer, Torches")
                    return

                # 가수와 노래 제목 파싱
                artist_name, song_name = map(str.strip, input_text.split(',', 1))

                # 데이터베이스에서 가사 조회
                lyrics = self.lyrics_handler.get_lyrics(artist_name, song_name)
                if not lyrics:
                    await ctx.send(f"'{artist_name}'의 '{song_name}' 가사가 데이터베이스에 없습니다.")
                    return

                # 데이터베이스에서 번역된 가사 조회
                translated_lyrics = self.translation_handler.get_translated_lyrics(artist_name, song_name)
                if translated_lyrics:
                    embed = discord.Embed(
                        title=f"'{artist_name}'의 '{song_name}' 번역된 가사",
                        description=translated_lyrics,
                        color=discord.Color.green()
                    )
                    await ctx.send("이미 번역된 가사가 있습니다:", embed=embed)
                    return

                # 번역 작업 시작
                await ctx.send(f"'{artist_name}'의 '{song_name}' 가사를 번역 중입니다. 잠시만 기다려주세요...")
                translated_lyrics = self.translation_handler.translate(lyrics)

                if not translated_lyrics:
                    await ctx.send("번역 작업 중 오류가 발생했습니다. 다시 시도해주세요.")
                    return

                # 번역 결과 저장
                self.translation_handler.save_translated_lyrics(artist_name, song_name, translated_lyrics)

                # 번역 결과 출력
                embed = discord.Embed(
                    title=f"'{artist_name}'의 '{song_name}' 번역된 가사",
                    description=translated_lyrics,
                    color=discord.Color.blue()
                )

                # 번역된 가사를 보여주는 Embed와 지우기 버튼
                delete_button = Button(label="지우기", style=discord.ButtonStyle.red)

                async def delete_callback(interaction):
                    if interaction.user == ctx.author:
                        await interaction.message.delete()
                    else:
                        await interaction.response.send_message(
                            "이 메시지는 작성자만 삭제할 수 있습니다.", ephemeral=True
                        )

                delete_button.callback = delete_callback

                view = View()
                view.add_item(delete_button)

                await ctx.send(embed=embed, view=view)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
