import re
import discord
from discord.ext import commands
from discord.ui import Button, View
from apis.genius_api import GeniusAPI
from apis.genius_crawling_api import GeniusCrawler  # 가사 크롤링 클래스

class GetArtistSongsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.genius_api = GeniusAPI()
        self.genius_crawler = GeniusCrawler()  # 가사 크롤러 인스턴스 생성
        self.song_list = []  # 노래 목록 저장

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='가수노래')
        async def artist_songs(ctx, *, artist_name: str):
            """아티스트의 모든 곡 제목을 번호와 함께 임베드로 표시하고 '삭제' 버튼 추가"""
            await ctx.send("곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.genius_api.search(artist_name)
                artist_ids = set()
                for hit in search_result['response']['hits']:
                    primary_artist_name = hit['result']['primary_artist']['name']
                    # 라틴어 및 프랑스어 문자가 포함되어 있는지 확인
                    if re.search(r'[\u00C0-\u017F]', primary_artist_name):
                        continue
                    if artist_name.lower() in primary_artist_name.lower():
                        artist_ids.add(hit['result']['primary_artist']['id'])

                if not artist_ids:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                self.song_list = []
                for artist_id in artist_ids:
                    # 아티스트의 곡 목록 가져오기
                    songs = await self.genius_api.get_artist_songs(artist_id, artist_name)
                    if songs:
                        self.song_list.extend(songs)

                if not self.song_list:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                # 곡 목록을 번호와 함께 4096자 이하로 분할하여 임베드 생성
                chunk_size = 4096
                chunks = []
                current_chunk = ""
                for idx, song in enumerate(self.song_list, 1):
                    song_title = song['title']
                    song_artist = song['primary_artist']['name']
                    entry = f"{idx}. {song_title} - {song_artist}\n"
                    if len(current_chunk) + len(entry) > chunk_size:
                        chunks.append(current_chunk)
                        current_chunk = entry
                    else:
                        current_chunk += entry
                if current_chunk:
                    chunks.append(current_chunk)

                # 각 청크를 별도의 임베드로 생성하여 전송
                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(
                        title=f"{artist_name}의 곡 목록 (페이지 {i+1}/{len(chunks)})",
                        description=chunk,
                        color=discord.Color.blue()
                    )

                    # 삭제 버튼 생성
                    delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

                    async def delete_message(interaction):
                        if interaction.user == ctx.author:
                            await interaction.message.delete()
                        else:
                            await interaction.response.send_message("이 메시지를 삭제할 권한이 없습니다.", ephemeral=True)

                    delete_button.callback = delete_message

                    view = View()
                    view.add_item(delete_button)

                    await ctx.send(embed=embed, view=view)

                # 번호 입력 대기
                await ctx.send("원하는 노래의 번호를 입력해주세요.")

                def check(m):
                    return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(self.song_list)

                msg = await self.bot.wait_for('message', check=check)
                song_index = int(msg.content) - 1
                song_url = self.song_list[song_index]['url']

                # 가사 크롤링
                lyrics = self.genius_crawler.request(song_url)
                if lyrics:
                    # 가사를 임베드로 전송
                    embed = discord.Embed(
                        title=f"{self.song_list[song_index]['title']}의 가사",
                        description=lyrics,
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("가사를 가져오는 데 실패했습니다.")

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
