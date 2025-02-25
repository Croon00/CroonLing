import discord
from discord.ui import Button, View
from service import SpotifyService


class RecommendationsButton(Button):
    def __init__(self, track):
        super().__init__(label="유사한 트랙 추천", style=discord.ButtonStyle.primary)
        self.spotify_service = SpotifyService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        # ✅ 유사한 트랙 가져오기
        recommended_tracks = await self.spotify_service.get_recommendations(self.track['song_id'])

        if not recommended_tracks:
            await interaction.followup.send("유사한 트랙을 가져오는 데 실패했습니다.")
            return

        # ✅ Embed 생성
        embed = discord.Embed(
            title=f"🎵 '{self.track['song_name']}'와 비슷한 트랙 추천",
            color=discord.Color.blue()
        )

        for track in recommended_tracks:
            embed.add_field(
                name=f"{track['song_name']} - {track['artist_name']}",
                value=f"🎧 [Spotify에서 듣기]({track['spotify_url']})\n"
                    f"🔥 인기도: {track['popularity']}",
                inline=False
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
