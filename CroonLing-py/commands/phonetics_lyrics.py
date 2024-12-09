import discord
from discord.ext import commands
from apis.translate_chatgpt_api import Translator
from discord.ui import Button, View


class PhoneticsLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='발음')
        async def phonetics_lyrics(ctx, *, query: str):
            """
            !!발음 (가수이름), (노래제목)
            - 데이터베이스에서 발음을 확인하고, 없으면 변환하여 저장한 뒤 Embed로 출력합니다.
            """
            try:
                # 입력된 가수와 곡 제목 파싱
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 입력해주세요. 예: !!발음 Aimer, Torches")
                return

            # 데이터베이스에서 발음 확인 및 처리
            try:
                lyrics, _, phonetics_lyrics, korean_phonetics = self.db_manager.get_lyrics(artist, song)

                if not lyrics:
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
                    return

                # 이미 발음이 있는 경우 Embed로 출력
                if phonetics_lyrics and korean_phonetics:
                    embed = discord.Embed(
                        title=f"{artist} - {song} 발음 변환 결과",
                        description=(
                            f"**로마자 발음:**\n{phonetics_lyrics}\n\n"
                            f"**한국어 발음:**\n{korean_phonetics}"
                        ),
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return

                # 발음 변환 로직 시작
                if not phonetics_lyrics:
                    phonetics_lyrics = self.translator.request(lyrics, request_type="phonetics")
                    if "오류가 발생했습니다" in phonetics_lyrics:
                        await ctx.send("로마자 발음 변환 중 오류가 발생했습니다.")
                        return
                    self.db_manager.update_phonetics(artist, song, phonetics_lyrics)

                if not korean_phonetics:
                    korean_phonetics = self.translator.request(phonetics_lyrics, request_type="roman_to_korean")
                    if "오류가 발생했습니다" in korean_phonetics:
                        await ctx.send("한국어 발음 변환 중 오류가 발생했습니다.")
                        return
                    self.db_manager.update_korean(artist, song, korean_phonetics)

                # 성공적으로 변환된 발음들을 Embed로 출력
                embed = discord.Embed(
                    title=f"{artist} - {song} 발음 변환 결과",
                    description=(
                        f"**로마자 발음:**\n{phonetics_lyrics}\n\n"
                        f"**한국어 발음:**\n{korean_phonetics}"
                    ),
                    color=discord.Color.purple()
                )

                # 지우기 버튼 추가
                delete_button = Button(label="지우기", style=discord.ButtonStyle.red)

                async def delete_button_callback(interaction):
                    if interaction.user == ctx.author:
                        await interaction.message.delete()
                    else:
                        await interaction.response.send_message("이 메시지는 작성자만 지울 수 있습니다.", ephemeral=True)

                delete_button.callback = delete_button_callback

                # View에 버튼 추가
                view = View()
                view.add_item(delete_button)

                await ctx.send(embed=embed, view=view)

            except Exception as e:
                await ctx.send(f"데이터베이스에서 발음을 처리하는 중 오류가 발생했습니다: {str(e)}")
