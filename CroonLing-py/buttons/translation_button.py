import discord
from discord.ui import Button
from service import (
    GetTranslationHandler,
    GetLyricsHandler,
    SaveHandler
    
)

class TranslationButton(Button):
    def __init__(self, track):
        super().__init__(label="번역", style=discord.ButtonStyle.primary)
        self.translation_handler = GetTranslationHandler()
        self.lyrics_handler = GetLyricsHandler()
        self.track = track
        self.save_handler = SaveHandler()

    async def callback(self, interaction):
        is_saved = self.save_handler.db_manager.is_song_saved(self.track['artist_name'], self.track['song_title'])
        if not is_saved:
            await interaction.response.send_message("해당 곡이 데이터베이스에 저장되어 있지 않습니다. 저장 버튼을 눌러 먼저 저장해주세요.")
            return

        translation = self.translation_handler.get_translated_lyrics(self.track['artist_name'], self.track['song_title'])
        if not translation:
            lyrics = self.lyrics_handler.get_lyrics(self.track['artist_name'], self.track['song_title'])
            if not lyrics:
                await interaction.response.send_message("데이터베이스에서 가사를 찾을 수 없습니다.")
                return

            translation = self.translation_handler.translate(lyrics)
            if not translation:
                await interaction.response.send_message("번역 작업 중 오류가 발생했습니다.")
                return

            self.translation_handler.save_translated_lyrics(self.track['artist_name'], self.track['song_title'], translation)

        embed = discord.Embed(
            title=f"'{self.track['song_title']}' 번역된 가사",
            description=translation,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
