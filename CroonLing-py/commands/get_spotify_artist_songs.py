import discord
from discord.ext import commands
from discord.ui import Button, View
from apis.spotify_api import SpotifyAPI  # Spotify API 클래스

class GetSpotifyArtistCommands:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_api = SpotifyAPI()

    def register(self):
        """Discord 봇에 명령어 등록"""
        
        @self.bot.command(name='스포티파이앨범')
        async def spotify_artist_albums(ctx, *, artist_name: str):
            """아티스트의 앨범을 목록으로 보여주고 선택한 앨범의 곡 목록을 표시"""
            await ctx.send("앨범 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                # 첫 번째 검색 결과의 아티스트 ID 사용
                artist_id = artists[0]['id']
                artist_name = artists[0]['name']

                # 아티스트의 앨범 목록 검색
                albums_result = await self.spotify_api.get(
                    f"artists/{artist_id}/albums",
                    params={"include_groups": "album", "limit": 50}
                )
                albums = albums_result.get('items', [])

                if not albums:
                    await ctx.send(f"'{artist_name}'의 앨범 정보를 찾을 수 없습니다.")
                    return

                # 앨범 목록 작성
                album_list = []
                for album in albums:
                    album_list.append({
                        'name': album['name'],
                        'release_date': album['release_date'],
                        'id': album['id']
                    })

                # 곡 목록을 번호와 함께 4096자 이하로 분할하여 임베드 생성
                chunk_size = 4096
                chunks = []
                current_chunk = ""
                for idx, album in enumerate(album_list, 1):
                    entry = f"{idx}. {album['name']} (발매일: {album['release_date']})\n"
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
                        title=f"{artist_name}의 앨범 목록 (페이지 {i+1}/{len(chunks)})",
                        description=chunk,
                        color=discord.Color.blue()
                    )
                    await ctx.send(embed=embed)

                # 앨범 번호 입력 대기
                await ctx.send("원하는 앨범의 번호를 입력해주세요.")

                def check(m):
                    return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(album_list)

                msg = await self.bot.wait_for('message', check=check)
                album_index = int(msg.content) - 1
                selected_album = album_list[album_index]

                # 선택한 앨범의 곡 목록 검색
                album_tracks_result = await self.spotify_api.get(f"albums/{selected_album['id']}/tracks")
                tracks = album_tracks_result.get('items', [])

                if not tracks:
                    await ctx.send(f"'{selected_album['name']}'의 곡 정보를 찾을 수 없습니다.")
                    return

                # 곡 목록 작성
                song_list = []
                for track in tracks:
                    song_list.append({
                        'title': track['name'],
                        'url': track['external_urls']['spotify']
                    })

                # 곡 목록을 번호와 함께 4096자 이하로 분할하여 임베드 생성
                chunks = []
                current_chunk = ""
                for idx, song in enumerate(song_list, 1):
                    entry = f"{idx}. {song['title']}\n"
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
                        title=f"{selected_album['name']}의 곡 목록 (페이지 {i+1}/{len(chunks)})",
                        description=chunk,
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")

        @self.bot.command(name='스포티파이싱글')
        async def spotify_artist_singles(ctx, *, artist_name: str):
            """아티스트의 싱글 곡 목록을 중복 없이 보여줌"""
            await ctx.send("싱글 곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                # 첫 번째 검색 결과의 아티스트 ID 사용
                artist_id = artists[0]['id']
                artist_name = artists[0]['name']

                # 아티스트의 싱글 목록 검색
                singles_result = await self.spotify_api.get(
                    f"artists/{artist_id}/albums",
                    params={"include_groups": "single", "limit": 50}
                )
                singles = singles_result.get('items', [])

                if not singles:
                    await ctx.send(f"'{artist_name}'의 싱글 곡 정보를 찾을 수 없습니다.")
                    return

                # 중복 없이 곡 목록 작성
                unique_singles = {}
                for single in singles:
                    tracks_result = await self.spotify_api.get(f"albums/{single['id']}/tracks")
                    tracks = tracks_result.get('items', [])
                    for track in tracks:
                        if track['name'] not in unique_singles:
                            unique_singles[track['name']] = {
                                'title': track['name'],
                                'url': track['external_urls']['spotify']
                            }

                # 곡 목록을 번호와 함께 4096자 이하로 분할하여 임베드 생성
                chunk_size = 4096
                chunks = []
                current_chunk = ""
                song_list = list(unique_singles.values())
                for idx, song in enumerate(song_list, 1):
                    entry = f"{idx}. {song['title']}\n"
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
                        title=f"{artist_name}의 싱글 곡 목록 (페이지 {i+1}/{len(chunks)})",
                        description=chunk,
                        color=discord.Color.orange()
                    )
                    await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
