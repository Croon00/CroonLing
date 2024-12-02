import discord
from discord.ext import commands
from discord.ui import Button, View
import httpx
from config_loader import load_config

# config.json 파일에서 설정 정보 불러오기
config = load_config()

class GetArtistSongsCommand:
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {config['GENIUS_API_TOKEN']}"}

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='가수노래')
        async def artist_songs(ctx, *, artist_name: str):
            """아티스트의 모든 곡 제목을 임베드로 표시"""
            await ctx.send("곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                artist_id = await self.search_artist(artist_name)
                if not artist_id:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                # 아티스트의 곡 목록 가져오기
                songs = await self.get_artist_songs(artist_id)
                if not songs:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                # 임베드 메시지 생성
                embed = discord.Embed(
                    title=f"{artist_name}의 곡 목록",
                    description="\n".join(songs),
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

    async def search_artist(self, artist_name):
        """아티스트 이름으로 아티스트 ID 검색"""
        endpoint = f"{self.base_url}/search"
        params = {"q": artist_name}
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            for hit in data['response']['hits']:
                if hit['result']['primary_artist']['name'].lower() == artist_name.lower():
                    return hit['result']['primary_artist']['id']
        return None

    async def get_artist_songs(self, artist_id, per_page=50):
        """아티스트 ID로 모든 곡 제목 가져오기"""
        songs = []
        page = 1
        while True:
            endpoint = f"{self.base_url}/artists/{artist_id}/songs"
            params = {
                "per_page": per_page,
                "page": page,
                "sort": "title"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                page_songs = data['response']['songs']
                if not page_songs:
                    break
                songs.extend([song['title'] for song in page_songs])
                page += 1
        return songs
