package com.croonling.lyricsservice.model.dto;

import com.croonling.lyricsservice.model.entity.Lyrics;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class LyricsResponseDto {
    private String songId;
    private String lyrics;
    private String translatedLyrics;
    private String phoneticsLyrics;
    private String phoneticsKoreanLyrics;
    private String kanjiInfo;

    @Builder
    public LyricsResponseDto(String songId, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics, String kanjiInfo) {
        this.songId = songId;
        this.lyrics = lyrics;
        this.translatedLyrics = translatedLyrics;
        this.phoneticsLyrics = phoneticsLyrics;
        this.phoneticsKoreanLyrics = phoneticsKoreanLyrics;
        this.kanjiInfo = kanjiInfo;
    }

    public static LyricsResponseDto fromEntity(Lyrics entity) {
        return LyricsResponseDto.builder()
                .songId(entity.getSongId())
                .lyrics(entity.getLyrics())
                .translatedLyrics(entity.getTranslatedLyrics())
                .phoneticsLyrics(entity.getPhoneticsLyrics())
                .phoneticsKoreanLyrics(entity.getPhoneticsKoreanLyrics())
                .kanjiInfo(entity.getKanjiInfo())
                .build();
    }
}