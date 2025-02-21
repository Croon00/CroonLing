import discord
from discord.ext import commands
from discord.ui import View
from service.spotify_service import SpotifyService
from service.song_service import SongService
from buttons import *
class FetchSingleSong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify_service = SpotifyService()
        self.song_service = SongService()

    @commands.command(name='곡하나')
    async def fetch_single_song(self, ctx, *, query: str):
        """!!곡하나 (가수이름), (곡제목) - 특정 곡 검색"""
        try:
            artist_name, song_name = map(str.strip, query.split(',', maxsplit=1))
        except ValueError:
            await ctx.send("올바른 형식으로 입력해주세요. 예: !!곡하나 BTS, Dynamite")
            return

        # 1️⃣ **DB에서 곡 정보 검색**
        song_data = self.song_service.get_song_info_by_artist_name(artist_name, song_name)

        if song_data:
            # 2️⃣ **DB에서 찾은 경우**
            embed = discord.Embed(
                title=f"{song_data['artist_name']} - {song_data['song_name']}",
                description=f"**앨범:** {song_data.get('album_name', '정보 없음')}\n"
                            f"**발매일:** {song_data.get('release_date', '정보 없음')}",
                color=discord.Color.blue()
            )
            if song_data.get("track_image_url"):
                embed.set_thumbnail(url=song_data["track_image_url"])
            await ctx.send(embed=embed)

            # 3️⃣ **버튼 추가**
            view = View()
            view.add_item(InfoButton(song_data))
            view.add_item(LyricsButton(song_data))
            view.add_item(TranslationButton(song_data))
            view.add_item(PhoneticsButton(song_data))
            view.add_item(PhoneticsKoreanButton(song_data))
            view.add_item(KanjiButton(song_data))
            view.add_item(EndButton(ctx.author.id, set()))

            # Spotify URL이 있다면 추가
            if song_data.get("url"):
                play_button = discord.ui.Button(label="재생", url=song_data["url"], style=discord.ButtonStyle.link)
                view.add_item(play_button)

            await ctx.send("원하는 정보를 선택하세요.", view=view)

        else:
            # 4️⃣ **DB에 없으면 Spotify API에서 검색**
            await ctx.send(f"'{artist_name} - {song_name}'의 정보를 찾을 수 없습니다. Spotify에서 검색 중...")

            song_data = await self.spotify_service.search_song(artist_name, song_name)
            if not song_data:
                await ctx.send(f"'{artist_name} - {song_name}'의 정보를 Spotify에서도 찾을 수 없습니다.")
                return

            # 5️⃣ **Spotify에서 검색된 곡 정보 표시**
            embed = discord.Embed(
                title=f"{song_data['artist_name']} - {song_data['song_name']}",
                description=f"**앨범:** {song_data.get('album_name', '정보 없음')}\n"
                            f"**발매일:** {song_data.get('release_date', '정보 없음')}",
                color=discord.Color.green()
            )
            if song_data.get("track_image_url"):
                embed.set_thumbnail(url=song_data["track_image_url"])
            await ctx.send(embed=embed)

            # 6️⃣ **버튼 추가 (사용자가 저장할 수 있도록)**
            view = View()
            view.add_item(SaveButton(song_data))  # 🎵 DB에 저장 버튼 추가
            view.add_item(EndButton(ctx.author.id, set()))  


            # Spotify URL이 있다면 추가
            if song_data.get("url"):
                play_button = discord.ui.Button(label="재생", url=song_data["url"], style=discord.ButtonStyle.link)
                view.add_item(play_button)

            await ctx.send("해당 곡을 데이터베이스에 저장하려면 '저장' 버튼을 눌러주세요.", view=view)

async def setup(bot):
    await bot.add_cog(FetchSingleSong(bot))
