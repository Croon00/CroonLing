import discord
from discord.ext import commands
import json
# from utils.logger import setup_logger
# from database.db import init_db
from apis.genius_api import GeniusAPI
from apis.genius_crawling_api import GeniusCrawler
from apis.translate_chatgpt_api import Translator
from commands.commands import CommandHandler

# config.json 파일을 읽어와서 토큰 값을 가져옵니다.
with open("config.json") as config_file:
    config = json.load(config_file)
    TOKEN = config['DISCORD_BOT_TOKEN']
    GENIUS_API_TOKEN = config['GENIUS_API_TOKEN']
    OPEN_API_TOKEN = config['OPEN_API_TOKEN']

# # 로깅 설정
# logger = setup_logger()

# # SQLite 데이터베이스 초기화
# conn, cursor = init_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

@bot.event
async def on_ready():
    # logger.info(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))



providers = {
    'genius_api': GeniusAPI(api_token=GENIUS_API_TOKEN),  # GENIUS API 인스턴스 생성
    'genius_crawler': GeniusCrawler(),
    'translator': Translator(api_key=OPEN_API_TOKEN),  # Translator 인스턴스를 딕셔너리에서 생성하면서 api_key 넘기기
}

command_handler = CommandHandler(bot, providers)
bot.run(TOKEN)

