import discord
from discord.ui import Button


class PhoneticsButton(Button):
    def __init__(self, phonetics_handler, track):
        super().__init__(label="발음", style=discord.ButtonStyle.primary)
        self.phonetics_handler = phonetics_handler
        self.track = track

    async def callback(self, interaction):
        pronunciation = self.phonetics_handler.get_phonetics(self.track['artist_name'], self.track['song_title'])
        await interaction.response.send_message(pronunciation if pronunciation else "저장되지 않은 발음입니다.")