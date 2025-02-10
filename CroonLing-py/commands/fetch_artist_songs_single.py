import discord
from discord.ext import commands
from apis import SpotifyAPI

class FetchArtistSongsSingle:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_api = SpotifyAPI()
        self.active_users = set()

    def register(self):
        @self.bot.command(name='싱글')
        async def spotify_artist_singles(ctx, *, artist_name: str):
            """아티스트의 싱글 목록을 보여줌"""
            if ctx.author.id in self.active_users:
                await ctx.send("이미 명령어를 실행 중입니다. 완료 후 다시 시도해주세요.")
                return

            self.active_users.add(ctx.author.id)
            await ctx.send("싱글 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                artist_id = artists[0]['id']
                artist_name = artists[0]['name']

                # 아티스트의 싱글 검색
                singles_result = await self.spotify_api.get(
                    f"artists/{artist_id}/albums",
                    params={"include_groups": "single", "limit": 50}
                )
                singles = singles_result.get('items', [])

                if not singles:
                    await ctx.send(f"'{artist_name}'의 싱글 정보를 찾을 수 없습니다.")
                    return

                single_list = [
                    {
                        'name': single['name'],
                        'release_date': single['release_date'],
                        'id': single['id'],
                        'album_image_url': single['images'][0]['url'] if single['images'] else None
                    }
                    for single in singles
                ]

                single_description = "\n".join(
                    [f"{idx + 1}. {single['name']} (발매일: {single['release_date']})"
                    for idx, single in enumerate(single_list)]
                )

                embed = discord.Embed(
                    title=f"{artist_name}의 싱글 목록",
                    description=single_description,
                    color=discord.Color.purple()
                )
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
            finally:
                self.active_users.discard(ctx.author.id)
