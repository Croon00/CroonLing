import discord
from discord.ui import Button, View
from service import TranslationService, LyricsService, SongService

class TranslationButton(Button):
    def __init__(self, track):
        super().__init__(label="번역", style=discord.ButtonStyle.primary)
        self.translation_service = TranslationService()
        self.lyrics_service = LyricsService()
        self.song_service = SongService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        # 곡이 DB에 저장되어 있는지 확인
        song_info = self.lyrics_service.get_song_info(self.track['artist_name'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        # 번역된 가사 확인
        translation = self.translation_service.get_translated_lyrics(self.track['song_id'])
        if not translation:
            lyrics = self.lyrics_service.get_lyrics(self.track['song_id'])

            if not lyrics:
                await interaction.followup.send("데이터베이스에서 가사를 찾을 수 없습니다.")
                return

            # 번역 요청
            await interaction.followup.send("가사를 번역 중입니다. 잠시만 기다려주세요...")
            translation = self.translation_service.translate_lyrics(self.track['song_id'], lyrics)  # ✅ 변경된 부분

            if not translation:
                await interaction.followup.send("번역 작업 중 오류가 발생했습니다.")
                return

        # 번역 결과 Embed로 표시
        embed = discord.Embed(
            title=f"'{self.track['song_name']}' 번역된 가사",
            description=translation,
            color=discord.Color.blue()
        )

        # "지우기" 버튼 추가
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
