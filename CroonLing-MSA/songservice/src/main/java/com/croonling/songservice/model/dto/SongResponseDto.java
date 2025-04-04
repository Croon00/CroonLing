package com.croonling.songservice.model.dto;

import com.croonling.songservice.model.entity.Song;
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
    private List<String> artistNames;
    private String albumName;
    private String releaseDate;
    private String trackImageUrl;
    private String url;
    private String lyrics;
    private String translatedLyrics;
    private String phoneticsLyrics;
    private String phoneticsKoreanLyrics;

    @Builder
    public SongResponseDto(String songId, List<String> songNames, String artistId, List<String> artistNames, String albumName, String releaseDate, String trackImageUrl, String url, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics) {
        this.songId = songId;
        this.songNames = songNames;
        this.artistId = artistId;
        this.artistNames = artistNames;
        this.albumName = albumName;
        this.releaseDate = releaseDate;
        this.trackImageUrl = trackImageUrl;
        this.url = url;
        this.lyrics = lyrics;
        this.translatedLyrics = translatedLyrics;
        this.phoneticsLyrics = phoneticsLyrics;
        this.phoneticsKoreanLyrics = phoneticsKoreanLyrics;
    }

    public static SongResponseDto fromEntity(Song song) {
        return SongResponseDto.builder()
                .songId(song.getSongId())
                .songNames(song.getSongNames())
                .artistId(song.getArtistId())
                .artistNames(song.getArtistNames())
                .albumName(song.getAlbumName())
                .releaseDate(song.getReleaseDate())
                .trackImageUrl(song.getTrackImageUrl())
                .url(song.getUrl())
                .lyrics(song.getLyrics())
                .translatedLyrics(song.getTranslatedLyrics())
                .phoneticsLyrics(song.getPhoneticsLyrics())
                .phoneticsKoreanLyrics(song.getPhoneticsKoreanLyrics())
                .build();
    }
}
