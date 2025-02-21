import discord
from discord.ext import commands
import json
import asyncio
from config_loader import load_config
from commands import __all__ as COGS  # ✅ commands/__init__.py에서 __all__ 가져오기

# config.json에서 토큰 로드
config = load_config()
TOKEN = config['DISCORD_BOT_TOKEN']

# Discord 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))

# ✅ `commands/__init__.py`의 `__all__`을 이용하여 모든 Cog 자동 로드
async def load_cogs():
    for cog in COGS:
        extension = f"commands.{cog}"
        try:
            await bot.load_extension(extension)
            print(f"✅ Cog 로드됨: {extension}")
        except Exception as e:
            print(f"❌ Cog 로드 실패: {extension} | 오류: {e}")

# ✅ 봇 실행
async def main():
    await load_cogs()  # Cog 자동 로드
    await bot.start(TOKEN)  # 봇 시작

asyncio.run(main())  # 비동기 실행
