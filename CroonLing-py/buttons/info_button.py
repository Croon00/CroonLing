import discord
from discord.ui import Button, View
from service.song_service import SongService

class InfoButton(Button):
    """ 곡의 정보 버튼 """

    def __init__(self, track):
        super().__init__(label="정보", style=discord.ButtonStyle.primary)
        self.song_service = SongService()
        self.track = track

    async def callback(self, interaction):
        """버튼 클릭 시 곡 정보를 조회하여 메시지로 전송"""
        info = self.song_service.get_song_info(self.track['artist_name'], self.track['song_name'])
        youtube_url = self.song_service.fetch_youtube_url(self.track['artist_name'], self.track['song_name'])  # ✅ 서비스에서 가져옴

        embed = discord.Embed(
            title=f"{info['song_name']} 정보" if info else "곡 정보",
            description=f"가수: {info['artist_name']}\n발매일: {info['release_date']}\n앨범 이름: {info['album_name']}" if info else "저장되지 않은 곡입니다.",
            color=discord.Color.blue()
        )
        if info and info.get('track_image_url'):
            embed.set_thumbnail(url=info['track_image_url'])

        view = View()
        delete_button = Button(label="지우기", style=discord.ButtonStyle.danger)

        async def delete_callback(delete_interaction):
            await delete_interaction.message.delete()

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        await interaction.response.send_message(embed=embed, view=view)
        if youtube_url:
            await interaction.followup.send(f"관련 YouTube 링크: {youtube_url}")
