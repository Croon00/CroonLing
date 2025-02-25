
import discord
from discord.ui import Button, View
from service import SpotifyService



class RelatedArtistsButton(Button):
    def __init__(self, track):
        super().__init__(label="유사한 아티스트", style=discord.ButtonStyle.primary)
        self.spotify_service = SpotifyService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        # ✅ 유사한 아티스트 가져오기
        related_artists = await self.spotify_service.get_related_artists(self.track['artist_id'])

        if not related_artists:
            await interaction.followup.send("유사한 아티스트를 가져오는 데 실패했습니다.")
            return

        # ✅ Embed 생성
        embed = discord.Embed(
            title=f"🎤 '{self.track['artist_name']}'와 비슷한 아티스트",
            color=discord.Color.purple()
        )

        for artist in related_artists:
            genres = ", ".join(artist["genres"]) if artist["genres"] else "장르 정보 없음"
            embed.add_field(
                name=artist["artist_name"],
                value=f"🔥 인기도: {artist['popularity']}\n🎼 장르: {genres}",
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