import discord
from discord.ui import Button, View
from service import GetInfoHandler, GetPhoneticsHandler, GetKoreanPhoneticsHandler
from apis.translate_chatgpt_api import Translator
from service.save_korean_phonetics_handler import SaveKoreanPhoneticsHandler

class KoreanPhoneticsButton(Button):
    def __init__(self, track):
        super().__init__(label="한국발음", style=discord.ButtonStyle.primary)
        self.info_handler = GetInfoHandler()
        self.phonetics_handler = GetPhoneticsHandler()
        self.korean_phonetics_handler = GetKoreanPhoneticsHandler()
        self.translator = Translator()
        self.save_korean_phonetics_handler = SaveKoreanPhoneticsHandler()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()
        song_info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        korean_pronunciation = self.korean_phonetics_handler.get_korean_phonetics(self.track['song_id'])
        if not korean_pronunciation:
            roman_pronunciation = self.phonetics_handler.get_phonetics(self.track['song_id'])
            if not roman_pronunciation:
                await interaction.followup.send("데이터베이스에서 로마자 발음을 찾을 수 없습니다.")
                return

            await interaction.followup.send("한국 발음을 생성 중입니다. 잠시만 기다려주세요...")
            korean_pronunciation = self.translator.roman_to_korean(roman_pronunciation)
            if not korean_pronunciation or "오류" in korean_pronunciation:
                await interaction.followup.send("한국 발음 생성 작업 중 오류가 발생했습니다.")
                return

            self.save_korean_phonetics_handler.save_korean_phonetics(self.track['song_id'], korean_pronunciation)

        embed = discord.Embed(
            title=f"'{self.track['song_name']}' 한국 발음",
            description=korean_pronunciation,
            color=discord.Color.orange()
        )
        view = View()

        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            await delete_interaction.message.delete()

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        await interaction.followup.send(embed=embed, view=view)
