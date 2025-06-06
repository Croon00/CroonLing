import discord
from discord.ext import commands
from service import ArtistsService  # ✅ ArtistsService 사용

class AddArtistNameKr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.artists_service = ArtistsService()  # ✅ 서비스 객체 사용

    @commands.command(name='가수이름입력')
    async def add_artist_name(self, ctx, *, artist_name: str):
        """
        !!가수이름입력 (가수이름)
        - 기존에 저장된 가수의 한국어 이름을 추가합니다.
        """
        try:
            # ✅ 1️⃣ DB에서 아티스트 조회
            artist_data = self.artists_service.get_artist_info(artist_name)
            if not artist_data["exists"]:
                await ctx.send(f"'{artist_name}' 가수를 데이터베이스에서 찾을 수 없습니다.")
                return

            artist_id = artist_data["artist_id"]  # 가수 ID 가져오기

            # ✅ 2️⃣ 한국어 가수 이름 입력 요청
            await ctx.send(f"추가할 '{artist_name}'의 한국어 이름을 입력해주세요:")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            # ✅ 3️⃣ 사용자 입력 받기
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                korean_artist_name = msg.content.strip()
            except asyncio.TimeoutError:
                await ctx.send("시간 초과로 요청이 취소되었습니다. 다시 시도해주세요.")
                return

            # ✅ 4️⃣ 한국어 이름 DB에 저장
            result = self.artists_service.add_artist_kr_name(artist_name, korean_artist_name)
            await ctx.send(result["message"])

        except Exception as e:
            await ctx.send(f"가수 이름을 처리하는 중 오류가 발생했습니다: {str(e)}")

# ✅ Cog 추가 함수
async def setup(bot):
    await bot.add_cog(AddArtistNameKr(bot))
