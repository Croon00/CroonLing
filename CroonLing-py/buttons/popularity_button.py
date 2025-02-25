import discord
from discord.ui import Button, View
from service import SpotifyService

class PopularityButton(Button):
    def __init__(self, track):
        super().__init__(label="트랙 인기도", style=discord.ButtonStyle.primary)
        self.spotify_service = SpotifyService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        # ✅ 트랙 인기도 가져오기
        popularity_info = await self.spotify_service.get_track_popularity(self.track['song_id'])

        if not popularity_info:
            await interaction.followup.send("트랙 인기도 정보를 가져오는 데 실패했습니다.")
            return

        # ✅ Embed 생성
        embed = discord.Embed(
            title=f"🎵 {popularity_info['song_name']} - {popularity_info['artist_name']}",
            description=f"**인기도 점수:** {popularity_info['popularity']}\n"
                        f"**상태:** {popularity_info['popularity_status']}",
            color=discord.Color.green()
        )

        # ✅ "지우기" 버튼 추가
        view = View()
        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            try:
                await delete_interaction.message.delete()
            except discord.NotFound:
                await delete_interaction.response.send_message("이미 삭제된 메시지입니다.", ephemeral=True)

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        await interaction.followup.send(embed=embed, view=view)