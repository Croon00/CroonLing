import discord
from discord.ext import commands
from database.db_manager import DBManager
from config_loader import load_config
from discord.ui import Button, View


# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class GetKoreanLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='한국발음')
        async def korean_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 데이터베이스에서 한국 발음을 조회"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!한국발음 Aimer, Torches")
                return

            # 데이터베이스에서 한국 발음 조회
            try:
                lyrics, _, _, korean_lyrics = self.db_manager.get_lyrics(artist, song)
                if korean_lyrics:
                    # 성공적으로 한국 발음을 가져온 경우
                    embed = discord.Embed(
                        title=f"{artist} - {song} 한국 발음",
                        description=f"**한국 발음:**\n{korean_lyrics}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                elif lyrics:
                    # 가사가 있지만 한국 발음이 없는 경우
                    await ctx.send(f"'{artist} - {song}'의 한국 발음이 데이터베이스에 없습니다.")
                else:
                    # 가사가 없는 경우
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
            except Exception as e:
                await ctx.send(f"데이터베이스에서 한국 발음을 조회하는 중 오류가 발생했습니다: {str(e)}")
                
        # 지우기 버튼 추가
            delete_button = Button(label="지우기", style=discord.ButtonStyle.red)

            async def delete_button_callback(interaction):
                    if interaction.user == ctx.author:
                        await interaction.message.delete()
                    else:
                        await interaction.response.send_message("이 메시지는 작성자만 지우기할 수 있습니다.", ephemeral=True)

            delete_button.callback = delete_button_callback

                # View에 버튼 추가
            view = View()
            view.add_item(delete_button)

            await ctx.send(embed=embed, view=view)            
