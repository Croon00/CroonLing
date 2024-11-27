import discord
from discord.ext import commands
import json
from apis import GeniusAPI, GeniusCrawler, Translator
from command_handler import CommandHandler


# print("한글이 잘 나오나")
# config.json 파일을 읽어와서 토큰 값을 가져옵니다.
with open("config.json") as config_file:
    config = json.load(config_file)
    TOKEN = config['DISCORD_BOT_TOKEN']
    GENIUS_API_TOKEN = config['GENIUS_API_TOKEN']
    OPEN_API_TOKEN = config['OPEN_API_TOKEN']

# Discord 봇 인스턴스 생성
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))

# Genius API, Genius Crawler, Translator 인스턴스 생성
genius_api_instance = GeniusAPI(api_token=GENIUS_API_TOKEN)
genius_crawler_instance = GeniusCrawler()
translator_instance = Translator(api_key=OPEN_API_TOKEN)

# CommandHandler 인스턴스 생성 및 명령어 등록
command_handler = CommandHandler(bot, genius_api_instance, genius_crawler_instance, translator_instance)

# Discord 봇 실행
bot.run(TOKEN)