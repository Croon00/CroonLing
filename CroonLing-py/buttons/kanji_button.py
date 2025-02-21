import discord
from discord.ui import Button, View
from service import KanjiService, LyricsService, SongService

class KanjiButton(Button):
    def __init__(self, track):
        super().__init__(label="한자", style=discord.ButtonStyle.primary)
        self.kanji_service = KanjiService()
        self.lyrics_service = LyricsService()
        self.song_service = SongService()
        self.track = track

    async def callback(self, interaction):
        await interaction.response.defer()

        # 곡이 DB에 저장되어 있는지 확인
        song_info = self.song_service.get_song_info(self.track['artist_id'], self.track['song_name'])
        if not song_info:
            await interaction.followup.send("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        # 한자 정보 확인
        kanji_info = self.kanji_service.get_kanji_info(self.track['song_id'])
        if not kanji_info:
            lyrics = self.lyrics_service.get_lyrics(self.track['song_id'])

            if not lyrics:
                await interaction.followup.send("데이터베이스에서 가사를 찾을 수 없습니다.")
                return

            # 한자 정보 요청
            await interaction.followup.send("가사에서 한자 정보를 추출 중입니다. 잠시만 기다려주세요...")
            kanji_info = self.kanji_service.lyrics_to_kanji(self.track['song_id'], lyrics)

            if not kanji_info:
                await interaction.followup.send("한자 정보 추출 중 오류가 발생했습니다.")
                return

        # 한자 정보 Embed로 표시
        embed = discord.Embed(
            title=f"'{self.track['song_name']}' 가사의 한자 정보",
            description=kanji_info,
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
