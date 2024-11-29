import discord
from discord.ext import commands
from database.db_manager import DBManager
from apis.translate_chatgpt_api import Translator
from apis.whisper_api import WhisperAPI
import os

class WhisperTranscriptionCommand:
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DBManager()
        self.translator = Translator()
        self.whisper_api = WhisperAPI()

    def register(self):
        """Discord 봇에 명령어 등록"""
        @self.bot.command(name='영상가사')
        async def transcribe_lyrics(ctx, *, query: str):
            """가수와 곡 제목을 입력받아 음성 파일에서 가사 추출 후 데이터베이스에 저장"""
            try:
                artist, song = query.split(',', maxsplit=1)
                artist = artist.strip()
                song = song.strip()
            except ValueError:
                await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!영상가사 Aimer, Torches")
                return

            file_path = f"downloads/{artist} - {song}.mp3"
            if not os.path.exists(file_path):
                await ctx.send(f"'{artist} - {song}'의 음성 파일을 찾을 수 없습니다. 먼저 !!영상 명령어를 사용해 주세요.")
                return

            await ctx.send("가사를 추출 중입니다...")

            try:
                # Whisper API 호출하여 음성 파일에서 가사 추출
                lyrics = self.whisper_api.transcribe_audio(file_path)

                # 추출된 가사 Discord로 전송
                await ctx.send(f"가사 추출 완료:\n{lyrics}")

                # 데이터베이스에 가사 저장
                self.db_manager.insert_song(artist, song, lyrics)

                # 한국어 번역 요청 및 DB에 저장
                translated_lyrics = self.translator.request(lyrics, request_type="translate")
                if "오류가 발생했습니다" not in translated_lyrics:
                    self.db_manager.update_translation(artist, song, translated_lyrics)
                    await ctx.send(f"한국어 번역 완료:\n{translated_lyrics}")
                else:
                    await ctx.send("번역 중 오류가 발생했습니다.")
            except Exception as e:
                await ctx.send(f"Whisper API를 통한 가사 추출 중 오류가 발생했습니다: {str(e)}")
