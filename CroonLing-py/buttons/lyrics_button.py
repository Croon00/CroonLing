import discord
from discord.ui import Button, View
from service import LyricsService, SongService

class LyricsButton(Button):
    def __init__(self, track):
        super().__init__(label="가사", style=discord.ButtonStyle.primary)
        self.song_service = SongService()
        self.lyrics_service = LyricsService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        song_info = self.song_service.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        lyrics = self.lyrics_service.get_lyrics(self.track['song_id'])
        if not lyrics:
            await interaction.followup.send(f"'{self.track['song_name']}'의 가사를 찾을 수 없어 구글에서 검색합니다...")
            lyrics = self.lyrics_service.fetch_and_save_lyrics(
                self.track['song_id'],  # ✅ `song_id`를 추가로 전달
                self.track['artist_name'],
                self.track['song_name']
            )
            if not lyrics:
                await interaction.followup.send(f"'{self.track['song_name']}'의 가사를 구글에서도 찾을 수 없습니다.")
                return

        embed = discord.Embed(
            title=f"{self.track['song_name']} - {self.track['artist_name']} 가사",
            description=lyrics,
            color=discord.Color.blue()
        )
        view = View()

        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            await delete_interaction.message.delete()

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        await interaction.followup.send(embed=embed, view=view)
