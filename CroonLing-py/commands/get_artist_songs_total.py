import discord
from discord.ext import commands
from discord.ui import Button, View
from apis.spotify_api import SpotifyAPI
from service.save_handler import SaveHandler
from service.info_handler import InfoHandler
from service.lyrics_handler import LyricsHandler
from service.translation_handler import TranslationHandler
from service.phonetics_handler import PhoneticsHandler
from service.korean_phonetics_handler import KoreanPhoneticsHandler
from service.song_name_handler import SongNameHandler


class GetSpotifyAllTracksCommands:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_api = SpotifyAPI()
        self.save_handler = SaveHandler()
        self.info_handler = InfoHandler()
        self.lyrics_handler = LyricsHandler()
        self.translation_handler = TranslationHandler()
        self.phonetics_handler = PhoneticsHandler()
        self.korean_phonetics_handler = KoreanPhoneticsHandler()
        self.song_name_handler = SongNameHandler()

    def register(self):
        @self.bot.command(name='모든곡')
        async def spotify_all_tracks(ctx, *, artist_name: str):
            """Spotify API를 통해 특정 가수의 모든 곡을 목록으로 보여줍니다."""
            await ctx.send(f"'{artist_name}'의 모든 곡 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

            try:
                # 아티스트 검색
                search_result = await self.spotify_api.search(artist_name, search_type="artist")
                artists = search_result.get('artists', {}).get('items', [])

                if not artists:
                    await ctx.send(f"'{artist_name}'에 대한 정보를 찾을 수 없습니다.")
                    return

                artist_id = artists[0]['id']
                artist_name = artists[0]['name']

                # 아티스트의 모든 트랙 검색
                tracks_result = await self.spotify_api.get(f"artists/{artist_id}/top-tracks", params={"market": "US"})
                tracks = tracks_result.get('tracks', [])

                if not tracks:
                    await ctx.send(f"'{artist_name}'의 곡 정보를 찾을 수 없습니다.")
                    return

                # 곡 목록 작성
                track_list = [
                    {'title': track['name'], 'url': track['external_urls']['spotify'], 'id': track['id']}
                    for track in tracks
                ]

                track_description = "\n".join(
                    [f"{idx + 1}. {track['title']}" for idx, track in enumerate(track_list)]
                )
                embed = discord.Embed(
                    title=f"{artist_name}의 모든 곡",
                    description=track_description,
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)

                await ctx.send("원하는 곡의 번호를 입력해주세요.")

                def track_check(m):
                    return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(track_list)

                track_msg = await self.bot.wait_for('message', check=track_check)
                track_index = int(track_msg.content) - 1
                selected_track = track_list[track_index]

                # 버튼 생성
                view = View()

                # 저장 버튼
                save_button = Button(label="저장", style=discord.ButtonStyle.primary)

                async def save_callback(interaction):
                    self.save_handler.save_artist_and_songs(
                        artist=artist_name,
                        album="Top Tracks",  # Spotify에서 가져온 상위 트랙 앨범으로 처리
                        songs=[selected_track]
                    )
                    await interaction.response.send_message(f"'{selected_track['title']}' 저장 완료.")

                save_button.callback = save_callback

                # 정보 버튼
                info_button = Button(label="정보", style=discord.ButtonStyle.primary)

                async def info_callback(interaction):
                    info = self.info_handler.get_song_info(artist_name, selected_track['title'])
                    if info:
                        embed = discord.Embed(
                            title=f"{info['song_name']} 정보",
                            description=(
                                f"가수: {info['artist_name']}\n"
                                f"발매일: {info['release_date']}\n"
                                f"인기도: {info['popularity']}\n"
                                f"[유튜브 링크]({info['youtube_link']})"
                            ),
                            color=discord.Color.blue()
                        )
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message("저장되지 않은 곡입니다.")

                info_button.callback = info_callback

                # 가사 버튼
                lyrics_button = Button(label="가사", style=discord.ButtonStyle.primary)

                async def lyrics_callback(interaction):
                    lyrics = self.lyrics_handler.get_lyrics(artist_name, selected_track['title'])
                    await interaction.response.send_message(lyrics if lyrics else "저장되지 않은 가사입니다.")

                lyrics_button.callback = lyrics_callback

                # 번역 버튼
                translation_button = Button(label="번역", style=discord.ButtonStyle.primary)

                async def translation_callback(interaction):
                    translation = self.translation_handler.get_translated_lyrics(artist_name, selected_track['title'])
                    await interaction.response.send_message(translation if translation else "저장되지 않은 번역입니다.")

                translation_button.callback = translation_callback

                # 발음 버튼
                pronunciation_button = Button(label="발음", style=discord.ButtonStyle.primary)

                async def pronunciation_callback(interaction):
                    pronunciation = self.phonetics_handler.get_phonetics(artist_name, selected_track['title'])
                    await interaction.response.send_message(pronunciation if pronunciation else "저장되지 않은 발음입니다.")

                pronunciation_button.callback = pronunciation_callback

                # 한국발음 버튼
                korean_pronunciation_button = Button(label="한국발음", style=discord.ButtonStyle.primary)

                async def korean_pronunciation_callback(interaction):
                    korean_pronunciation = self.korean_phonetics_handler.get_korean_phonetics(
                        artist_name, selected_track['title']
                    )
                    await interaction.response.send_message(
                        korean_pronunciation if korean_pronunciation else "저장되지 않은 한국 발음입니다."
                    )

                korean_pronunciation_button.callback = korean_pronunciation_callback

                # 곡 이름 입력 버튼
                song_name_button = Button(label="곡 이름 입력", style=discord.ButtonStyle.primary)

                async def song_name_callback(interaction):
                    await interaction.response.send_message("새 곡 이름을 입력하세요.")

                    def name_check(m):
                        return m.author == interaction.user

                    msg = await self.bot.wait_for('message', check=name_check)
                    new_name = msg.content
                    self.song_name_handler.update_song_name(selected_track['id'], new_name)
                    await interaction.followup.send(f"곡 이름이 '{new_name}'으로 업데이트되었습니다.")

                song_name_button.callback = song_name_callback

                # 버튼 추가
                for button in [
                    save_button, info_button, lyrics_button, translation_button,
                    pronunciation_button, korean_pronunciation_button, song_name_button
                ]:
                    view.add_item(button)

                # 재생 버튼은 URL 연결
                play_button = Button(label="재생", url=selected_track['url'], style=discord.ButtonStyle.link)
                view.add_item(play_button)

                await ctx.send(f"'{selected_track['title']}'을(를) 선택하셨습니다.", view=view)

            except Exception as e:
                await ctx.send(f"오류 발생: {str(e)}")
