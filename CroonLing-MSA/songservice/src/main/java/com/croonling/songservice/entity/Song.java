package com.croonling.songservice.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Arrays;
import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "songs")
public class Song {
    @Id
    @Column(name = "song_id", unique = true)
    private String songId;

    @Column(columnDefinition = "TEXT")  // 🔹 쉼표로 구분된 문자열 저장
    private String songNames;

    @Column(name = "artist_id", nullable = false)
    private String artistId;

    @Column(name = "album_name", nullable = true)
    private String albumName;

    @Column(name = "release_date", nullable = false)
    private String releaseDate;

    @Column(name = "track_image_url", nullable = true)
    private String trackImageUrl;


    private String url;
    private String lyrics;
    private String translatedLyrics;
    private String phoneticsLyrics;
    private String phoneticsKoreanLyrics;

    // 🔹 `songNames`를 List<String>으로 변환하는 메서드
    public List<String> getSongNamesList() {
        return songNames != null ? Arrays.asList(songNames.split(",")) : null;
    }

    public void setSongNamesList(List<String> names) {
        this.songNames = names != null ? String.join(",", names) : null;
    }

    @Builder
    public Song(String songId, String songNames, String artistId, String albumName, String releaseDate, String trackImageUrl, String url, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics) {
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
