import discord
from discord.ext import commands
from database.db_manager import DBManager


class SongNameInputCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()

    @commands.command(name='곡이름입력')
    async def input_song_name(self, ctx, *, query: str):
        """
        !!곡이름입력 (가수이름), (노래제목)
        - DB에서 가수 이름과 노래 제목으로 곡을 찾은 후, 한국어 곡 이름을 입력받아 저장합니다.
        """
        try:
            # 입력된 가수와 곡 제목 파싱
            artist, song = query.split(',', maxsplit=1)
            artist = artist.strip()
            song = song.strip()
        except ValueError:
            await ctx.send("올바른 형식으로 입력해주세요. 예: !!곡이름입력 Aimer, Torches")
            return

        # DB에서 해당 곡 확인
        try:
            song_data = self.db_manager.get_song_info(artist, song)
            if not song_data:
                await ctx.send(f"'{artist} - {song}' 곡을 데이터베이스에서 찾을 수 없습니다.")
                return

            song_id = song_data['song_id']  # 해당 곡의 song_id 가져오기

            # 한국어 곡 이름 입력 요청
            await ctx.send("추가할 한국어 곡 이름을 입력해주세요:")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            # 사용자 입력 기다림
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                korean_song_name = msg.content.strip()
            except asyncio.TimeoutError:
                await ctx.send("시간 초과로 요청이 취소되었습니다. 다시 시도해주세요.")
                return

            # 한국어 곡 이름 DB에 저장
            success = self.db_manager.insert_song_name_kr(song_id, korean_song_name)
            if success:
                await ctx.send(f"'{artist} - {song}'에 한국어 곡 이름 '{korean_song_name}'이(가) 추가되었습니다.")
            else:
                await ctx.send("데이터베이스에 저장하는 중 오류가 발생했습니다. 다시 시도해주세요.")

        except Exception as e:
            await ctx.send(f"곡 이름을 처리하는 중 오류가 발생했습니다: {str(e)}")


# Cog 추가 함수
def setup(bot):
    bot.add_cog(SongNameInputCommand(bot))
