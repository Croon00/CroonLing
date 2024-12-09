import discord
from discord.ui import Button
from service.get_info_handler import GetInfoHandler
from service.save_song_handler import SaveHandler


class SaveButton(Button):
    def __init__(self, track):
        super().__init__(label="저장", style=discord.ButtonStyle.primary)
        self.get_info_handler = GetInfoHandler()  # GetInfoHandler를 사용
        self.save_handler = SaveHandler()
        self.track = track

    async def callback(self, interaction):
        # Interaction을 진행 중으로 표시
        await interaction.response.defer()

        # "저장 중..." 메시지 표시
        saving_message = await interaction.followup.send("저장 중...")

        # 곡 정보가 DB에 저장되어 있는지 확인
        song_info = self.get_info_handler.get_song_info(
            self.track['artist_name'], self.track['song_name']
        )

        if song_info:
            # 곡 정보가 이미 있는 경우
            await saving_message.edit(content="이미 저장된 곡입니다.")
        else:
            # 저장 로직 수행
            self.save_handler.save_track(self.track)
            await saving_message.edit(content="저장 완료!")
