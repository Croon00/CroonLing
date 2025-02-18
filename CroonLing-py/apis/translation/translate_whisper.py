# # -*- coding: utf-8 -*-
# import openai
# import json
# import openai.error
# from .api_interface import APIInterface
# from config_loader import load_config


# class WhisperTranscriptionCommand:
#     def __init__(self, bot):
#         self.bot = bot
#         self.db_manager = DBManager()
#         self.translator = Translator()

#     def register(self):
#         """Discord 봇에 명령어 등록"""
#         @self.bot.command(name='영상가사')
#         async def transcribe_lyrics(ctx, *, query: str):
#             """가수와 곡 제목을 입력받아 음성 파일에서 가사 추출 후 데이터베이스에 저장"""
#             try:
#                 artist, song = query.split(',', maxsplit=1)
#                 artist = artist.strip()
#                 song = song.strip()
#             except ValueError:
#                 await ctx.send("올바른 형식으로 가수와 곡 제목을 입력해주세요. 예: !!영상가사 Aimer, Torches")
#                 return

#             file_path = f"downloads/{artist} - {song}.mp3"
#             if not os.path.exists(file_path):
#                 await ctx.send(f"'{artist} - {song}'의 음성 파일을 찾을 수 없습니다. 먼저 !!영상 명령어를 사용해 주세요.")
#                 return

#             await ctx.send("가사를 추출 중입니다...")

#             try:
#                 audio_file = open(file_path, "rb")
#                 transcript = openai.Audio.transcribe("whisper-1", audio_file)
#                 lyrics = transcript['text']
#                 audio_file.close()

#                 await ctx.send(f"가사 추출 완료:\n{lyrics}")
#                 self.db_manager.insert_song(artist, song, lyrics)

#                 # 한국어 번역 요청 및 DB에 저장
#                 translated_lyrics = self.translator.request(lyrics, request_type="translate")
#                 if "오류가 발생했습니다" not in translated_lyrics:
#                     self.db_manager.update_translation(artist, song, translated_lyrics)
#                     await ctx.send(f"한국어 번역 완료:\n{translated_lyrics}")
#                 else:
#                     await ctx.send("번역 중 오류가 발생했습니다.")
#             except Exception as e:
#                 await ctx.send(f"Whisper API를 통한 가사 추출 중 오류가 발생했습니다: {str(e)}")

# # Discord 봇 인스턴스 생성 및 명령어 등록
# bot = commands.Bot(command_prefix='!!', intents=discord.Intents.default())

# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user.name}')
#     await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="!!명령어 로 도움말 확인"))

# # 명령어 인스턴스 생성 및 등록
# youtube_command = YoutubeDownloadCommand(bot)
# youtube_command.register()

# whisper_command = WhisperTranscriptionCommand(bot)
# whisper_command.register()

# # Discord 봇 실행
# token = config['DISCORD_BOT_TOKEN']
# bot.run(token)