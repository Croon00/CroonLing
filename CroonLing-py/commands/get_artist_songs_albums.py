import discord
from discord.ext import commands
from discord.ui import View
from apis.spotify_api import SpotifyAPI
from buttons import (
    SaveButton,
    InfoButton,
    LyricsButton,
    TranslationButton,
    PhoneticsButton,
    KoreanPhoneticsButton,
    EndButton,
)

class GetSpotifyArtistAlbumsCommands:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_api = SpotifyAPI()
        self.active_users = set()  # 명령어 실행 중인 사용자 목록

    def register(self):
        @self.bot.command(name='앨범')
        async def spotify_artist_albums(ctx, *, artist_name: str):
            """아티스트의 앨범 목록을 보여주고 선택한 앨범의 곡 목록을 표시"""
            if ctx.author.id in self.active_users:
                await ctx.send("이미 명령어를 실행 중입니다. 완료 후 다시 시도해주세요.")
                return

            self.active_users.add(ctx.author.id)
            await ctx.send("앨범 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

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

                album_list = [
                    {
                        'name': album['name'],
                        'release_date': album['release_date'],
                        'id': album['id'],
                        'album_image_url': album['images'][0]['url'] if album['images'] else None
                    }
                    for album in albums
                ]
                album_description = "\n".join(
                    [f"{idx + 1}. {album['name']} (발매일: {album['release_date']})"
                     for idx, album in enumerate(album_list)]
                )
                embed = discord.Embed(
                    title=f"{artist_name}의 앨범 목록",
                    description=album_description,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

                await ctx.send("원하는 앨범의 번호를 입력해주세요.")

                def check(m):
                    return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(album_list)

                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=20)  # 20초 제한
                    album_index = int(msg.content) - 1
                    selected_album = album_list[album_index]
                except asyncio.TimeoutError:
                    await ctx.send("시간이 초과되었습니다. 명령어를 다시 실행해주세요.")
                    self.active_users.discard(ctx.author.id)  # 사용자 상태 해제
                    return

                # 선택한 앨범의 곡 목록 검색
                album_tracks_result = await self.spotify_api.get(f"albums/{selected_album['id']}/tracks")
                tracks = album_tracks_result.get('items', [])

                if not tracks:
                    await ctx.send(f"'{selected_album['name']}'의 곡 정보를 찾을 수 없습니다.")
                    return

                
                # 곡 리스트 생성
                song_list = [
                    {
                        'artist_id': artist_id,
                        'artist_name': artist_name,
                        'album_name': selected_album['name'],
                        'song_id': track['id'],
                        'song_name': track['name'],
                        'release_date': selected_album['release_date'],
                        'track_image_url': selected_album['album_image_url'],
                        'url': track['external_urls']['spotify'] if 'external_urls' in track and 'spotify' in track['external_urls'] else None,
                    }
                    for track in tracks
                ]
                
                track_description = "\n".join(
                    [f"{idx + 1}. {song['song_name']}" for idx, song in enumerate(song_list)]
                )
                embed = discord.Embed(
                    title=f"{selected_album['name']}의 곡 목록",
                    description=track_description,
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)

                await ctx.send("원하는 곡의 번호를 입력해주세요.")

                def track_check(m):
                    return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(song_list)

                try:
                    track_msg = await self.bot.wait_for('message', check=track_check, timeout=20)  # 20초 제한
                    track_index = int(track_msg.content) - 1
                    selected_track = song_list[track_index]
                except asyncio.TimeoutError:
                    await ctx.send("시간이 초과되었습니다. 명령어를 다시 실행해주세요.")
                    self.active_users.discard(ctx.author.id)  # 사용자 상태 해제
                    return

                # 버튼 생성
                view = View()
                view.add_item(SaveButton(selected_track))
                view.add_item(InfoButton(selected_track))
                view.add_item(LyricsButton(selected_track))
                view.add_item(TranslationButton(selected_track))
                view.add_item(PhoneticsButton(selected_track))
                view.add_item(KoreanPhoneticsButton(selected_track))

                # 끝내기 버튼 추가
                view.add_item(EndButton(ctx.author.id, self.active_users))

                # 재생 버튼은 URL 연결
                play_button = discord.ui.Button(label="재생", url=selected_track['url'], style=discord.ButtonStyle.link)
                view.add_item(play_button)

                await ctx.send(f"'{selected_track['song_name']}'을(를) 선택하셨습니다.", view=view)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
            finally:
                self.active_users.discard(ctx.author.id)  # 명령어 실행 상태 해제
