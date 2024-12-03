import discord
from discord.ext import commands
from discord.ui import Button, View
from apis.genius_api import GeniusAPI

class GetArtistSongsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.genius_api = GeniusAPI()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='가수노래')
        async def artist_songs(ctx, *, artist_name: str):
            """아티스트의 모든 곡 제목을 임베드로 표시하고 '삭제' 버튼 추가"""
            await ctx.send("곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.genius_api.search(artist_name)
                artist_id = None
                for hit in search_result['response']['hits']:
                    if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                        artist_id = hit['result']['primary_artist']['id']
                        break

                if not artist_id:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                # 아티스트의 곡 목록 가져오기
                songs = await self.genius_api.get_artist_songs(artist_id)
                if not songs:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                # 곡 목록을 4096자 이하로 분할하여 임베드 생성
                chunk_size = 4096
                chunks = []
                current_chunk = ""
                for song in songs:
                    if len(current_chunk) + len(song) + 1 > chunk_size:
                        chunks.append(current_chunk)
                        current_chunk = song + "\n"
                    else:
                        current_chunk += song + "\n"
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
                    delete_button = Button(label="삭제", style=discord.ButtonStyle.danger)

                    async def delete_message(interaction):
                        if interaction.user == ctx.author:
                            await interaction.message.delete()
                        else:
                            await interaction.response.send_message("이 메시지를 삭제할 권한이 없습니다.", ephemeral=True)

                    delete_button.callback = delete_message

                    view = View()
                    view.add_item(delete_button)

                    await ctx.send(embed=embed, view=view)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
