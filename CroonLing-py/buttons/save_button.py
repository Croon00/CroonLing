import discord
from discord.ui import Button
from service.get_lyrics_handler import GetLyricsHandler


class SaveButton(Button):
    def __init__(self, save_handler, track):
        super().__init__(label="저장", style=discord.ButtonStyle.primary)
        self.save_handler = save_handler
        self.track = track
        self.get_lyrics_handler = GetLyricsHandler()

    async def callback(self, interaction):
        # 이미 저장된 곡인지 확인 (get_lyrics_handler 사용)
        lyrics = self.get_lyrics_handler.get_lyrics(
            self.track['artist_name'], self.track['song_title']
        )

        if lyrics:
            await interaction.response.send_message("이미 저장된 곡입니다.")
        else:
            # 저장 로직 수행
            result = self.save_handler.save_tracks([self.track])
            saved_count = len(result['saved_tracks'])
            duplicate_count = len(result['duplicate_tracks'])
            await interaction.response.send_message(
                f"저장 완료: {saved_count}개, 중복된 트랙: {duplicate_count}개"
            )
