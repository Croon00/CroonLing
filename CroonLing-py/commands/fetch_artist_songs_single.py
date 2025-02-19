import discord
from discord.ext import commands
from discord.ui import View
from service.spotify_service import SpotifyService
from buttons import SaveButton, InfoButton, LyricsButton, TranslationButton, PhoneticsButton, PhoneticsKoreanButton, EndButton

class FetchArtistSongsSingle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify_service = SpotifyService()
        self.active_users = set()

    @commands.command(name='싱글')
    async def spotify_artist_singles(self, ctx, *, artist_name: str):
        """아티스트의 싱글 목록을 보여주고 선택할 수 있도록 함"""
        if ctx.author.id in self.active_users:
            await ctx.send("이미 명령어를 실행 중입니다. 완료 후 다시 시도해주세요.")
            return

        self.active_users.add(ctx.author.id)
        await ctx.send("싱글 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

        try:
            # 아티스트 검색
            artist = await self.spotify_service.get_artist_info(artist_name)
            if not artist:
                await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                return

            artist_id = artist["artist_id"]
            artist_name = artist["artist_name"]

            # 싱글 목록 검색
            singles = await self.spotify_service.get_singles_by_artist(artist_id)
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

            await ctx.send("원하는 싱글의 번호를 입력해주세요.")

            def check(m):
                return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(single_list)

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=20)
                single_index = int(msg.content) - 1
                selected_single = single_list[single_index]
            except asyncio.TimeoutError:
                await ctx.send("시간이 초과되었습니다. 명령어를 다시 실행해주세요.")
                self.active_users.discard(ctx.author.id)
                return

            # 버튼을 통한 곡 선택 기능 추가
            view = View()
            view.add_item(SaveButton(selected_single))
            view.add_item(InfoButton(selected_single))
            view.add_item(LyricsButton(selected_single))
            view.add_item(TranslationButton(selected_single))
            view.add_item(PhoneticsButton(selected_single))
            view.add_item(PhoneticsKoreanButton(selected_single))
            view.add_item(EndButton(ctx.author.id, self.active_users))

            # Spotify 재생 버튼 추가
            play_button = discord.ui.Button(label="재생", url=selected_single['album_image_url'], style=discord.ButtonStyle.link)
            view.add_item(play_button)

            await ctx.send(f"'{selected_single['name']}'을(를) 선택하셨습니다.", view=view)

        except Exception as e:
            await ctx.send(f"오류 발생: {str(e)}")
        finally:
            self.active_users.discard(ctx.author.id)

# ✅ Cog 추가 함수
async def setup(bot):
    await bot.add_cog(FetchArtistSongsSingle(bot))