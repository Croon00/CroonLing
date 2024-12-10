import discord
from discord.ui import Button, View
from service import GetInfoHandler
import requests
import re

class InfoButton(Button):
    def __init__(self, track):
        super().__init__(label="정보", style=discord.ButtonStyle.primary)
        self.info_handler = GetInfoHandler()
        self.track = track

    def fetch_youtube_url(self, artist_name, song_name):
        query = f"{artist_name} {song_name}"
        search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
            if video_ids:
                return f"https://www.youtube.com/watch?v={video_ids[0]}"
        except requests.RequestException as e:
            print(f"YouTube 검색 중 오류 발생: {e}")

        return None

    async def callback(self, interaction):
        info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_name'])
        youtube_url = self.fetch_youtube_url(self.track['artist_name'], self.track['song_name'])

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
