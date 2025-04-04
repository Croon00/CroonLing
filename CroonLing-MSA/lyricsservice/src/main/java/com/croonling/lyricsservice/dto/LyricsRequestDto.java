package com.croonling.lyricsservice.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LyricsRequestDto {
    private String songId;
    private String lyrics;
    private String translatedLyrics;
    private String phoneticsLyrics;
    private String phoneticsKoreanLyrics;
    private String kanjiInfo;
}
