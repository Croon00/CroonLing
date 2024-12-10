import discord
from discord.ui import Button, View
from service import GetInfoHandler, GetPhoneticsHandler
from apis.translate_chatgpt_api import Translator
from service.save_phonetics_handler import SavePhoneticsHandler
from service.get_lyrics_handler import GetLyricsHandler

class PhoneticsButton(Button):
    def __init__(self, track):
        super().__init__(label="발음", style=discord.ButtonStyle.primary)
        self.info_handler = GetInfoHandler()
        self.phonetics_handler = GetPhoneticsHandler()
        self.translator = Translator()
        self.save_phonetics_handler = SavePhoneticsHandler()
        self.get_lyrics_handler = GetLyricsHandler()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()
        song_info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        pronunciation = self.phonetics_handler.get_phonetics(self.track['song_id'])
        if not pronunciation:
            lyrics = self.get_lyrics_handler.get_lyrics(self.track['song_id'])
            if not lyrics:
                await interaction.followup.send("데이터베이스에서 가사를 찾을 수 없습니다.")
                return

            await interaction.followup.send("발음을 생성 중입니다. 잠시만 기다려주세요...")
            pronunciation = self.translator.phonetics(lyrics)
            if not pronunciation or "오류" in pronunciation:
                await interaction.followup.send("발음 생성 작업 중 오류가 발생했습니다.")
                return

            self.save_phonetics_handler.save_phonetics(self.track['song_id'], pronunciation)

        embed = discord.Embed(
            title=f"'{self.track['song_name']}' 발음",
            description=pronunciation,
            color=discord.Color.green()
        )
        view = View()

        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            await delete_interaction.message.delete()

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        await interaction.followup.send(embed=embed, view=view)
