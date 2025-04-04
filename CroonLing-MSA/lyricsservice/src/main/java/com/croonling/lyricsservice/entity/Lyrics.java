package com.croonling.lyricsservice.entity;// com.croonling.lyricsservice.model.entity.Lyrics.java

import jakarta.persistence.*;
import lombok.*;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "lyrics")
public class Lyrics {

    @Id
    @Column(name = "song_id", nullable = false, unique = true)
    private String songId;

    @Lob
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

    @Lob
    @Column(name = "kanji_info")
    private String kanjiInfo;

    @Builder
    public Lyrics(String songId, String lyrics, String translatedLyrics, String phoneticsLyrics, String phoneticsKoreanLyrics, String kanjiInfo) {
        this.songId = songId;
        this.lyrics = lyrics;
        this.translatedLyrics = translatedLyrics;
        this.phoneticsLyrics = phoneticsLyrics;
        this.phoneticsKoreanLyrics = phoneticsKoreanLyrics;
        this.kanjiInfo = kanjiInfo;
    }
}
