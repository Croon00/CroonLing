import discord
from discord.ext import commands
from database.db_manager import DBManager
from config_loader import load_config
from apis.translate_chatgpt_api import Translator
from discord.ui import Button, View

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

class PhoneticsLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()
        self.translator = Translator()

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
                lyrics, translated_lyrics, phonetics_lyrics, korean = self.db_manager.get_lyrics(artist, song)
                
                
                
                if lyrics:
                    # 발음 변환 로직 시작
                    if not phonetics_lyrics:
                        # 로마자 발음 변환 요청
                        phonetics_lyrics = self.translator.request(lyrics, request_type="phonetics")
                        if "오류가 발생했습니다" not in phonetics_lyrics:
                            self.db_manager.update_phonetics(artist, song, phonetics_lyrics)
                        else:
                            await ctx.send(f"로마자 발음 변환 중 오류가 발생했습니다.")
                            return

            
                    # 한국어 발음 변환 로직
                    if not korean:
                        korean = self.translator.request(phonetics_lyrics, request_type="roman_to_korean")
                        if "오류가 발생했습니다" not in korean:
                            self.db_manager.update_korean(artist, song, korean)
                        else:
                            await ctx.send(f"한국어 발음 변환 중 오류가 발생했습니다.")
                            return

                    # 성공적으로 변환된 발음들을 포함한 메시지 출력
                    embed = discord.Embed(
                        title=f"{artist} - {song} 발음 변환 결과",
                        description=f"**로마자 발음:**\n{phonetics_lyrics}",
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"'{artist} - {song}'의 가사를 데이터베이스에서 찾을 수 없습니다.")
            except Exception as e:
                await ctx.send(f"데이터베이스에서 가사를 조회하거나 발음 변환하는 중 오류가 발생했습니다: {str(e)}")
                
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