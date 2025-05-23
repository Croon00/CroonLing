import asyncio
import threading
import logging
from fastapi import FastAPI
import discord
from discord.ext import commands
from config_loader import load_config
from commands import __all__ as COGS  # ✅ Cog 목록 불러오기

# 📌 FastAPI 앱 생성
app = FastAPI()

# 📌 로깅 설정
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("🚀 Railway 컨테이너 실행 시작!")

# 📌 Discord 설정
config = load_config()
TOKEN = config['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"✅ Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))

# 📌 Cog 자동 로드
async def load_cogs():
    for cog in COGS:
        extension = f"commands.{cog}"
        try:
            await bot.load_extension(extension)
            logging.info(f"✅ Cog 로드됨: {extension}")
        except Exception as e:
            logging.error(f"❌ Cog 로드 실패: {extension} | 오류: {e}")

# 📌 Discord Bot 실행 함수 (스레드용)
def run_discord_bot():
    asyncio.run(bot_main())

async def bot_main():
    await load_cogs()
    await bot.start(TOKEN)

# 📌 FastAPI 엔드포인트 (간단한 health check용)
@app.get("/")
async def root():
    return {"message": "CroonLing Discord Bot is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# 📌 Discord Bot 백그라운드 실행
threading.Thread(target=run_discord_bot).start()
