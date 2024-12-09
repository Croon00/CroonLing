import discord
from discord.ui import Button
from service.get_info_handler import GetInfoHandler
from service.save_lyrics import SaveLyricsService
from service.get_lyrics_handler import GetLyricsHandler

class LyricsButton(Button):
    def __init__(self, track):
        super().__init__(label="가사", style=discord.ButtonStyle.primary)
        self.get_info_handler = GetInfoHandler()  # GetInfoHandler로 변경
        self.get_lyrics_handler = GetLyricsHandler()
        self.save_lyrics_service = SaveLyricsService()
        self.track = track

    async def callback(self, interaction):
        # 곡이 DB에 저장되어 있는지 확인
        song_info = self.get_info_handler.get_song_info(
            self.track['artist_name'], self.track['song_name']
        )

        if not song_info:
            # 곡이 DB에 없는 경우
            await interaction.response.send_message(
                "해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요."
            )
            return

        # 가사를 데이터베이스에서 조회
        lyrics = self.get_lyrics_handler.get_lyrics(
            self.track['artist_name'], self.track['song_name']
        )

        if lyrics:
            # 가사가 이미 존재하는 경우 Embed로 표시
            embed = discord.Embed(
                title=f"{self.track['song_name']} - {self.track['artist_name']} 가사",
                description=lyrics,
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        else:
            # 가사가 없는 경우 구글에서 검색 후 저장
            await interaction.response.send_message(
                f"'{self.track['song_name']}'의 가사를 찾을 수 없어 구글에서 검색합니다..."
            )
            lyrics = self.save_lyrics_service.fetch_and_save_lyrics(
                self.track['artist_name'], self.track['song_name']
            )
            if lyrics:
                embed = discord.Embed(
                    title=f"{self.track['song_name']} - {self.track['artist_name']} 가사",
                    description=lyrics,
                    color=discord.Color.green()
                )
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"'{self.track['song_name']}'의 가사를 구글에서도 찾을 수 없습니다."
                )
