import discord
from discord.ui import Button, View
from service import (
    GetTranslationHandler,
    GetLyricsHandler,
    GetInfoHandler,  # GetInfoHandler를 사용
    SaveTranslationHandler
)
from apis.translate_chatgpt_api import Translator  # 번역 API 클래스 가져오기

class TranslationButton(Button):
    def __init__(self, track):
        super().__init__(label="번역", style=discord.ButtonStyle.primary)
        self.translation_handler = GetTranslationHandler()
        self.lyrics_handler = GetLyricsHandler()
        self.info_handler = GetInfoHandler()  # GetInfoHandler 인스턴스 생성
        self.translator = Translator()  # Translator 인스턴스 생성
        self.track = track
        self.save_translated_lyrics = SaveTranslationHandler()

    async def callback(self, interaction):
        # Interaction 처리 시작
        await interaction.response.defer()

        # 곡이 데이터베이스에 저장되어 있는지 확인
        song_info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        # 번역된 가사 확인
        translation = self.translation_handler.get_translated_lyrics(self.track['song_id'])
        if not translation:
            # 가사 가져오기
            lyrics = self.lyrics_handler.get_lyrics(self.track['song_id'])
            print(lyrics)

            if not lyrics:
                await interaction.followup.send("데이터베이스에서 가사를 찾을 수 없습니다.")
                return

            # 번역 요청
            await interaction.followup.send("가사를 번역 중입니다. 잠시만 기다려주세요...")
            translation = self.translator.translate(lyrics)
            if not translation or "오류" in translation:
                await interaction.followup.send("번역 작업 중 오류가 발생했습니다.")
                return

            # 번역된 가사 저장
            self.save_translated_lyrics.save_translated_lyrics(self.track['song_id'], translation)

        # 번역 결과를 Embed로 표시
        embed = discord.Embed(
            title=f"'{self.track['song_name']}' 번역된 가사",
            description=translation,
            color=discord.Color.blue()
        )

        # View 생성
        view = View()

        # "지우기" 버튼 추가
        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            try:
                await delete_interaction.message.delete()
            except discord.NotFound:
                await delete_interaction.response.send_message("이미 삭제된 메시지입니다.", ephemeral=True)

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        # 메시지 전송
        await interaction.followup.send(embed=embed, view=view)
