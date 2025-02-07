import discord
from discord.ui import Button

class EndButton(Button):
    """ 명령 끝내는 버튼

    Args:
        Button (_type_): _description_
        author_id (str): 사용자 고유 ID
        active_users: 사용자 상태
        
    """
    def __init__(self, author_id, active_users):
        super().__init__(label="끝내기", style=discord.ButtonStyle.danger)
        self.author_id = author_id
        self.active_users = active_users

    async def callback(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("이 버튼은 해당 사용자만 사용할 수 있습니다.", ephemeral=True)
            return

        self.active_users.discard(self.author_id)  # 사용자 상태 해제
        await interaction.response.send_message("명령어를 종료했습니다.")
        self.view.stop()  # 뷰 중단
