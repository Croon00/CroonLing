import discord
from discord.ext import commands
import json
from utils.logger import setup_logger
from database.db import init_db
from api.genius_api import GeniusAPI
from commands.command import CommandHandler

# config.json 파일을 읽어와서 토큰 값을 가져옵니다.
with open("config.json") as config_file:
    config = json.load(config_file)
    TOKEN = config['DISCORD_TOKEN']
    GENIUS_TOKEN = config['GENIUS_TOKEN']

# 로깅 설정
logger = setup_logger()

# SQLite 데이터베이스 초기화
conn, cursor = init_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))

# Genius API 초기화
genius_api = GeniusAPI(GENIUS_TOKEN)

# 커맨드 설정
command_handler = CommandHandler(bot, genius_api)

bot.run(TOKEN)
