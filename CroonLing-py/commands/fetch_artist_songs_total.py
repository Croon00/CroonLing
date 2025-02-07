import discord
from discord.ext import commands
from apis.spotify_api import SpotifyAPI

class FetchArtistSongsTotal:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_api = SpotifyAPI()
        self.active_users = set()

    def register(self):
        @self.bot.command(name='전체곡')
        async def spotify_artist_all_songs(ctx, *, artist_name: str):
            """아티스트의 모든 곡 목록을 보여줌"""
            if ctx.author.id in self.active_users:
                await ctx.send("이미 명령어를 실행 중입니다. 완료 후 다시 시도해주세요.")
                return

            self.active_users.add(ctx.author.id)
            await ctx.send("전체 곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                artist_id = artists[0]['id']
                artist_name = artists[0]['name']

                # 아티스트의 모든 앨범 가져오기
                albums_result = await self.spotify_api.get(
                    f"artists/{artist_id}/albums",
                    params={"include_groups": "album,single", "limit": 50}
                )
                albums = albums_result.get('items', [])

                if not albums:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                song_list = []
                for album in albums:
                    album_tracks_result = await self.spotify_api.get(f"albums/{album['id']}/tracks")
                    tracks = album_tracks_result.get('items', [])
                    song_list.extend([
                        {
                            'name': track['name'],
                            'album': album['name'],
                            'release_date': album['release_date']
                        }
                        for track in tracks
                    ])

                if not song_list:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                songs_description = "\n".join(
                    [f"{idx + 1}. {song['name']} (앨범: {song['album']}, 발매일: {song['release_date']})"
                    for idx, song in enumerate(song_list)]
                )

                embed = discord.Embed(
                    title=f"{artist_name}의 전체 곡 목록",
                    description=songs_description,
                    color=discord.Color.gold()
                )
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
            finally:
                self.active_users.discard(ctx.author.id)
