package com.croonling.songservice.converter;

import com.croonling.songservice.dto.SongRequestDto;
import com.croonling.songservice.dto.SongResponseDto;
import com.croonling.songservice.entity.Song;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;

@Component
public class SongConverter {

    // ✅ DTO → Entity 변환
    public Song toEntity(SongRequestDto dto) {
        return Song.builder()
                .songId(dto.getSongId())
                .songNames(String.join(",", dto.getSongNames()))  // 🔹 List<String> → String 변환
                .artistId(dto.getArtistId())
                .albumName(dto.getAlbumName())
                .releaseDate(dto.getReleaseDate())
                .trackImageUrl(dto.getTrackImageUrl())
                .url(dto.getUrl())
                .lyrics(dto.getLyrics())
                .translatedLyrics(dto.getTranslatedLyrics())
                .phoneticsLyrics(dto.getPhoneticsLyrics())
                .phoneticsKoreanLyrics(dto.getPhoneticsKoreanLyrics())
                .build();
    }

    // ✅ Entity → DTO 변환
    public SongResponseDto toResponse(Song song) {
        return SongResponseDto.builder()
                .songId(song.getSongId())
                .songNames(Arrays.asList(song.getSongNames().split(",")))  // 🔹 String → List<String> 변환
                .artistId(song.getArtistId())
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
