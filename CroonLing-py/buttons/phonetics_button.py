import discord
from discord.ui import Button, View
from service import SongService, PhoneticsService

class PhoneticsButton(Button):
    def __init__(self, track):
        super().__init__(label="발음", style=discord.ButtonStyle.primary)
        self.song_service = SongService()
        self.phonetics_service = PhoneticsService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        song_info = self.song_service.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        pronunciation = self.phonetics_service.get_phonetics(self.track['song_id'])
        if not pronunciation:
            await interaction.followup.send("데이터베이스에서 발음을 찾을 수 없습니다. 발음을 생성 중입니다. 잠시만 기다려주세요...")

            # ✅ 서비스에서 발음 생성 요청
            pronunciation = self.phonetics_service.generate_and_save_phonetics(self.track['song_id'])
            if not pronunciation:
                await interaction.followup.send("발음 생성 작업 중 오류가 발생했습니다.")
                return

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
