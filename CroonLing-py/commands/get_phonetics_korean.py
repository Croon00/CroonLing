import discord
from discord.ext import commands
from apis import Translator
from discord.ui import Button, View


class GetPhoneticsKorean:
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='한국발음')
        async def korean_lyrics(ctx, *, query: str):
            """
            !!한국발음 (가수이름), (노래제목)
            - 데이터베이스에서 로마자 발음을 확인한 뒤, 이를 한국어 발음으로 변환하여 출력합니다.
            """
            try:
                # 입력된 가수와 곡 제목 파싱
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 입력해주세요. 예: !!한국발음 Aimer, Torches")
                return

            # 데이터베이스에서 로마자 발음 조회 및 처리
            try:
                lyrics, _, phonetics_lyrics, korean_lyrics = self.db_manager.get_lyrics(artist, song)

                if not lyrics:
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
                    return

                if not phonetics_lyrics:
                    await ctx.send(f"'{artist} - {song}'의 로마자 발음이 데이터베이스에 없습니다. 먼저 '!!발음' 명령어를 사용하여 발음을 생성해주세요.")
                    return

                # 이미 한국 발음이 있는 경우 Embed로 출력
                if korean_lyrics:
                    embed = discord.Embed(
                        title=f"{artist} - {song} 한국 발음",
                        description=f"**한국 발음:**\n{korean_lyrics}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return

                # 한국 발음 생성 로직
                korean_lyrics = self.translator.request(phonetics_lyrics, request_type="roman_to_korean")
                if "오류가 발생했습니다" in korean_lyrics:
                    await ctx.send("한국 발음 생성 중 오류가 발생했습니다.")
                    return

                # DB에 한국 발음 저장
                self.db_manager.update_korean(artist, song, korean_lyrics)

                # 성공적으로 변환된 발음을 Embed로 출력
                embed = discord.Embed(
                    title=f"{artist} - {song} 한국 발음",
                    description=f"**한국 발음:**\n{korean_lyrics}",
                    color=discord.Color.blue()
                )

                # 지우기 버튼 추가
                delete_button = Button(label="지우기", style=discord.ButtonStyle.red)

                async def delete_button_callback(interaction):
                    if interaction.user == ctx.author:
                        await interaction.message.delete()
                    else:
                        await interaction.response.send_message(
                            "이 메시지는 작성자만 지울 수 있습니다.", ephemeral=True
                        )

                delete_button.callback = delete_button_callback

                # View에 버튼 추가
                view = View()
                view.add_item(delete_button)

                await ctx.send(embed=embed, view=view)

            except Exception as e:
                await ctx.send(f"데이터베이스에서 한국 발음을 처리하는 중 오류가 발생했습니다: {str(e)}")
