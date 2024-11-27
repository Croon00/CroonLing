import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord.ui import Button, View
from database.db_manager import DBManager  # 새로 만든 DB 클래스 가져오기
from pymysql import MySQLError

# config.json 파일에서 DB 설정 정보 불러오기
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

class GetGoogleLyricsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager(config)

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='구글가사')
        async def get_google_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 구글에서 가사 검색"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!구글가사 Aimer, Torches")
                return

            search_query = f"{artist} {song} lyrics"
            search_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            try:
                response = requests.get(search_url, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                await ctx.send(f"구글 검색 중 오류가 발생했습니다: {str(e)}")
                return

            soup = BeautifulSoup(response.text, "html.parser")

            # 진짜 노래 제목 추출
            lyrics_title = soup.find("div", class_="PZPZlf ssJ7i B5dxMb")
            if lyrics_title:
                real_title = lyrics_title.get_text(strip=True)
            else:
                real_title = song  # 제목을 못 찾은 경우 사용자가 입력한 제목 사용

            # 가사 부분의 여러 섹션들을 모두 탐색
            lyrics_divs = soup.find_all("div", class_="ujudUb")

            if not lyrics_divs:
                await ctx.send(f"'{artist} - {song}'의 가사를 찾을 수 없습니다.")
                return

            lyrics = ""
            for div in lyrics_divs:
                spans = div.find_all("span", jsname="YS01Ge")
                for span in spans:
                    lyrics += span.text + "\n"

            if lyrics.strip():
                # 가사 결과를 Discord Embed로 전송
                embed = discord.Embed(
                    title=f"{artist} - {real_title} 가사",
                    description=lyrics,
                    color=discord.Color.blue()
                )

                # 삭제 버튼 추가
                delete_button = Button(label="삭제", style=discord.ButtonStyle.red)

                async def delete_button_callback(interaction):
                    if interaction.user == ctx.author:
                        await interaction.message.delete()
                    else:
                        await interaction.response.send_message("이 메시지는 작성자만 삭제할 수 있습니다.", ephemeral=True)

                delete_button.callback = delete_button_callback

                # View에 버튼 추가
                view = View()
                view.add_item(delete_button)

                await ctx.send(embed=embed, view=view)
                
                # MySQL에 연결 한 후 데이터 삽입
                try:
                    self.db_manager.insert_song(artist, real_title, lyrics)
                except MySQLError as e:
                    await ctx.send(f"데이터베이스에 저장 중 오류가 발생했습니다: {str(e)}")
            else:
                await ctx.send(f"'{artist} - {song}'의 가사를 찾을 수 없습니다.")
