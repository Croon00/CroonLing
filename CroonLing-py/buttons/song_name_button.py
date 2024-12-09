# import discord
# from discord.ui import Button


# class SongNameButton(Button):
#     def __init__(self, song_name_handler, track):
#         super().__init__(label="곡 이름 입력", style=discord.ButtonStyle.primary)
#         self.song_name_handler = song_name_handler
#         self.track = track

#     async def callback(self, interaction):
#         await interaction.response.send_message("새 곡 이름을 입력하세요.")

#         def name_check(m):
#             return m.author == interaction.user

#         msg = await self.bot.wait_for('message', check=name_check)
#         new_name = msg.content
#         self.song_name_handler.update_song_name(self.track['song_id'], new_name)
#         await interaction.followup.send(f"곡 이름이 '{new_name}'으로 업데이트되었습니다.")
