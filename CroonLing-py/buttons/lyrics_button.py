import discord
from discord.ui import Button
from service.save_lyrics import SaveLyricsService


class LyricsButton(Button):
    def __init__(self, save_lyrics_service, track):
        super().__init__(label="가사", style=discord.ButtonStyle.primary)
        self.save_lyrics_service = save_lyrics_service
        self.track = track

    async def callback(self, interaction):
        # 가사를 데이터베이스에서 먼저 조회
        lyrics = self.save_lyrics_service.get_lyrics(
            self.track['artist_name'], self.track['song_title']
        )

        if lyrics:
            await interaction.response.send_message(lyrics)
        else:
            # 가사가 없을 경우 구글에서 검색 후 저장
            await interaction.response.send_message(
                f"'{self.track['song_title']}'의 가사를 찾을 수 없어 구글에서 검색합니다..."
            )
            lyrics = self.save_lyrics_service.fetch_and_save_lyrics(
                self.track['artist_name'], self.track['song_title']
            )
            if lyrics:
                await interaction.followup.send(
                    f"가사를 성공적으로 저장하고 가져왔습니다:\n\n{lyrics}"
                )
            else:
                await interaction.followup.send(
                    f"'{self.track['song_title']}'의 가사를 구글에서도 찾을 수 없습니다."
                )
