import os
import requests
import openai
import yt_dlp as youtube_dl  # yt-dlp 사용
import discord
from discord.ext import commands
from database.db_manager import DBManager
from config_loader import load_config
from apis.translate_chatgpt_api import Translator

# config.json 파일에서 설정 정보 불러오기
config = load_config()
openai.api_key = config['OPEN_API_TOKEN']

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

class YoutubeDownloadCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='영상')
        async def download_video(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 유튜브에서 영상을 검색 및 다운로드 후 변환"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!영상 Aimer, Torches")
                return

            search_query = f"{artist} {song}"
            search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(search_query)}"

            response = requests.get(search_url)
            if response.status_code != 200:
                await ctx.send("유튜브 검색 중 오류가 발생했습니다.")
                return

            video_id = response.text.split('watch?v=')[1].split('"')[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            await ctx.send(f"유튜브에서 영상을 찾았습니다: {video_url}\n다운로드 중입니다...")

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    file_name = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                await ctx.send(f"다운로드 및 변환 완료: {file_name}")
            except Exception as e:
                await ctx.send(f"영상 다운로드 또는 변환 중 오류가 발생했습니다: {str(e)}")

