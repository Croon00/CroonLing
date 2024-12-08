import discord
from discord.ext import commands
from database.db_manager import DBManager


class ArtistNameInputCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()

    @commands.command(name='가수이름입력')
    async def input_artist_name(self, ctx, *, artist_name: str):
        """
        !!가수이름입력 (가수이름)
        - DB에서 가수 이름을 확인한 후, 한국어 이름을 입력받아 저장합니다.
        """
        try:
            # DB에서 가수 확인
            artist_data = self.db_manager.get_artist_info(artist_name)
            if not artist_data:
                await ctx.send(f"'{artist_name}' 가수를 데이터베이스에서 찾을 수 없습니다.")
                return

            artist_id = artist_data['artist_id']  # 가수 ID 가져오기

            # 한국어 가수 이름 입력 요청
            await ctx.send(f"추가할 '{artist_name}'의 한국어 이름을 입력해주세요:")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            # 사용자 입력 기다림
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                korean_artist_name = msg.content.strip()
            except asyncio.TimeoutError:
                await ctx.send("시간 초과로 요청이 취소되었습니다. 다시 시도해주세요.")
                return

            # 한국어 가수 이름 DB에 저장
            success = self.db_manager.insert_artist_name_kr(artist_id, korean_artist_name)
            if success:
                await ctx.send(f"'{artist_name}'에 한국어 이름 '{korean_artist_name}'이(가) 추가되었습니다.")
            else:
                await ctx.send("데이터베이스에 저장하는 중 오류가 발생했습니다. 다시 시도해주세요.")

        except Exception as e:
            await ctx.send(f"가수 이름을 처리하는 중 오류가 발생했습니다: {str(e)}")


# Cog 추가 함수
def setup(bot):
    bot.add_cog(ArtistNameInputCommand(bot))
