import discord
from discord.ui import Button
from service import GetKoreanPhoneticsHandler

class KoreanPhoneticsButton(Button):
    def __init__(self, track):
        super().__init__(label="한국발음", style=discord.ButtonStyle.primary)
        self.korean_phonetics_handler = GetKoreanPhoneticsHandler()
        self.track = track

    async def callback(self, interaction):
        korean_pronunciation = self.korean_phonetics_handler.get_korean_phonetics(
            self.track['artist_name'], self.track['song_title']
        )
        await interaction.response.send_message(
            korean_pronunciation if korean_pronunciation else "저장되지 않은 한국 발음입니다."
        )
