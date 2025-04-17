import logging
import discord
from discord.ui import Button
from service import SongService

class SaveButton(Button):
    def __init__(self, track):
        super().__init__(label="저장", style=discord.ButtonStyle.primary)
        self.song_service = SongService()
        self.track = track
        logging.info(f"✅ SaveButton 생성됨 - 곡명: {self.track['song_name']}")

    async def callback(self, interaction):
        try:
            # Interaction을 진행 중으로 표시
            await interaction.response.defer()
            logging.info(f"🔹 '{self.track['song_name']}' 저장 버튼 클릭됨1")

            # "저장 중..." 메시지 표시
            saving_message = await interaction.followup.send("저장 중...")
            logging.info(f"🔹 '{self.track['song_name']}' 저장 버튼 클릭됨2")

            # 곡 정보가 DB에 저장되어 있는지 확인
            song_info = await self.song_service.get_song_info(
                self.track['artist_id'], self.track['song_name']
            )
            logging.info(f"🔹 '{self.track['song_name']}'곡 저장되는지 확인")

            if song_info:
                logging.warning(f"⚠️ 이미 저장된 곡: {self.track['song_name']}")
                await saving_message.edit(content="이미 저장된 곡입니다.")
            else:
                # 저장 로직 수행
                await self.song_service.save_track(self.track)
                logging.info(f"✅ 곡 저장 완료: {self.track['song_name']}")
                await saving_message.edit(content="저장 완료!")

        except Exception as e:
            logging.error(f"🚨 저장 버튼 실행 중 오류 발생 - 곡명: {self.track['song_name']} | 오류: {e}", exc_info=True)
            await interaction.followup.send("❌ 오류 발생! 관리자에게 문의하세요.")
