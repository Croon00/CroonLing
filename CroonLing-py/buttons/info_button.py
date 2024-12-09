import discord
from discord.ui import Button
from service import GetInfoHandler
import requests
import re


class InfoButton(Button):
    def __init__(self, track):
        super().__init__(label="정보", style=discord.ButtonStyle.primary)
        self.info_handler = GetInfoHandler()
        self.track = track

    def fetch_youtube_url(self, artist_name, song_name):
        """YouTube 검색 결과에서 첫 번째 URL 가져오기"""
        query = f"{artist_name} {song_name}"
        search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            # HTML 소스에서 동영상 URL 추출
            video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
            if video_ids:
                return f"https://www.youtube.com/watch?v={video_ids[0]}"
        except requests.RequestException as e:
            print(f"YouTube 검색 중 오류 발생: {e}")

        return None

    async def callback(self, interaction):
        info = self.info_handler.get_song_info(self.track['artist_name'], self.track['song_name'])
        youtube_url = self.fetch_youtube_url(self.track['artist_name'], self.track['song_name'])

        if info:
            embed = discord.Embed(
                title=f"{info['song_name']} 정보",
                description=(
                    f"가수: {info['artist_name']}\n"
                    f"발매일: {info['release_date']}\n"
                    f"앨범 이름: {info['album_name']}\n"
                ),
                color=discord.Color.blue()
            )
            if info.get('track_image_url'):
                embed.set_thumbnail(url=info['track_image_url'])

            await interaction.response.send_message(embed=embed)

            if youtube_url:
                await interaction.followup.send(f"관련 YouTube 링크: {youtube_url}")
            else:
                await interaction.followup.send("YouTube 링크를 찾을 수 없습니다.")
        else:
            await interaction.response.send_message("저장되지 않은 곡입니다.")
