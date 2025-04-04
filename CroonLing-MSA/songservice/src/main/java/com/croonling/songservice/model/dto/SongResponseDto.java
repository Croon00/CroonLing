package com.croonling.songservice.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@NoArgsConstructor
@Getter
public class SongResponseDto {
    private String songId;
    private List<String> songNames;
    private String artistId;
    private String albumName;
    private String releaseDate;
    private String trackImageUrl;
    private String url;
    private String lyrics;
    private String translatedLyrics;
    private String phoneticsLyrics;
    private String phoneticsKoreanLyrics;

    @Builder
    public SongResponseDto(String songId, List<String> songNames, String artistId, String albumName, String releaseDate, String trackImageUrl, String url, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics) {
        this.songId = songId;
        this.songNames = songNames;
        this.artistId = artistId;
        this.albumName = albumName;
        this.releaseDate = releaseDate;
        this.trackImageUrl = trackImageUrl;
        this.url = url;
        this.lyrics = lyrics;
        this.translatedLyrics = translatedLyrics;
        this.phoneticsLyrics = phoneticsLyrics;
        this.phoneticsKoreanLyrics = phoneticsKoreanLyrics;
    }
}
