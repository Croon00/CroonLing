import discord
from discord.ext import commands
from discord.ui import View
from service.spotify_service import SpotifyService
from buttons import *
class FetchArtistSongsTotal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify_service = SpotifyService()
        self.active_users = set()

    @commands.command(name='전체곡')
    async def spotify_artist_all_songs(self, ctx, *, artist_name: str):
        """아티스트의 모든 곡 목록을 보여주고 선택할 수 있도록 함"""
        if ctx.author.id in self.active_users:
            await ctx.send("이미 명령어를 실행 중입니다. 완료 후 다시 시도해주세요.")
            return

        self.active_users.add(ctx.author.id)
        await ctx.send("전체 곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

        try:
            # 아티스트 검색
            artist = await self.spotify_service.get_artist_info(artist_name)
            if not artist:
                await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                return

            artist_id = artist["artist_id"]
            artist_name = artist["artist_name"]

            # 모든 곡 목록 검색
            all_songs = await self.spotify_service.get_all_songs_by_artist(artist_id)
            if not all_songs:
                await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                return

            song_list = [
                {
                    "song_name": song["song_name"],
                    "album_name": song["album_name"],
                    "release_date": song["release_date"]
                }
                for song in all_songs
            ]

            songs_description = "\n".join(
                [f"{idx + 1}. {song['song_name']} (앨범: {song['album_name']}, 발매일: {song['release_date']})"
                 for idx, song in enumerate(song_list)]
            )

            embed = discord.Embed(
                title=f"{artist_name}의 전체 곡 목록",
                description=songs_description,
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)

            await ctx.send("원하는 곡의 번호를 입력해주세요.")

            def check(m):
                return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(song_list)

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=20)
                song_index = int(msg.content) - 1
                selected_song = song_list[song_index]
            except asyncio.TimeoutError:
                await ctx.send("시간이 초과되었습니다. 명령어를 다시 실행해주세요.")
                self.active_users.discard(ctx.author.id)
                return

            # 버튼을 통한 곡 선택 기능 추가
            view = View()
            view.add_item(SaveButton(selected_song))
            view.add_item(InfoButton(selected_song))
            view.add_item(LyricsButton(selected_song))
            view.add_item(TranslationButton(selected_song))
            view.add_item(PhoneticsButton(selected_song))
            view.add_item(PhoneticsKoreanButton(selected_song))
            view.add_item(KanjiButton(selected_song))
            view.add_item(EndButton(ctx.author.id, self.active_users))

            # Spotify 재생 버튼 추가
            play_button = discord.ui.Button(label="재생", url="https://open.spotify.com/", style=discord.ButtonStyle.link)
            view.add_item(play_button)

            await ctx.send(f"'{selected_song['song_name']}'을(를) 선택하셨습니다.", view=view)

        except Exception as e:
            await ctx.send(f"오류 발생: {str(e)}")
        finally:
            self.active_users.discard(ctx.author.id)

# ✅ Cog 추가 함수
async def setup(bot):
    await bot.add_cog(FetchArtistSongsTotal(bot))