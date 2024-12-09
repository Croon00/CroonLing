import discord
from discord.ui import Button


class InfoButton(Button):
    def __init__(self, info_handler, track):
        super().__init__(label="정보", style=discord.ButtonStyle.primary)
        self.info_handler = info_handler
        self.track = track

    async def callback(self, interaction):
        info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_title'])
        if info:
            embed = discord.Embed(
                title=f"{info['song_name']} 정보",
                description=(
                    f"가수: {info['artist_name']}\n"
                    f"발매일: {info['release_date']}\n"
                    f"[유튜브 링크]({info['youtube_link']})"
                ),
                color=discord.Color.blue()
            )
            if info.get('track_image_url'):
                embed.set_thumbnail(url=info['track_image_url'])
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("저장되지 않은 곡입니다.")
