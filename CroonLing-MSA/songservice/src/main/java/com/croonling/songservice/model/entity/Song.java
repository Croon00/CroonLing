package com.croonling.songservice.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "songs")
public class Song {
    @Id
    @Column(name = "song_id", unique = true, nullable = false)
    private String songId;

    @ElementCollection  // 🔹 List<String> 자동 매핑
    @CollectionTable(name = "song_names", joinColumns = @JoinColumn(name = "song_id"))
    @Column(name = "song_name")
    private List<String> songNames;

    @Column(name = "artist_id", nullable = false)
    private String artistId;

    @ElementCollection
    @CollectionTable(name = "song_artist_names", joinColumns = @JoinColumn(name = "song_id"))
    @Column(name = "artist_name")
    private List<String> artistNames;

    @Column(name = "album_name")
    private String albumName;

    @Column(name = "release_date")
    private String releaseDate;

    @Column(name = "track_image_url")
    private String trackImageUrl;

    @Column(name = "url")
    private String url;

    @Lob  // 🔹 긴 문자열 데이터 처리
    @Column(name = "lyrics")
    private String lyrics;

    @Lob
    @Column(name = "translated_lyrics")
    private String translatedLyrics;

    @Lob
    @Column(name = "phonetics_lyrics")
    private String phoneticsLyrics;

    @Lob
    @Column(name = "phonetics_korean_lyrics")
    private String phoneticsKoreanLyrics;

    @Builder
    public Song(String songId, List<String> songNames, String artistId, List<String> artistNames, String albumName, String releaseDate, String trackImageUrl, String url, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics) {
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
}
