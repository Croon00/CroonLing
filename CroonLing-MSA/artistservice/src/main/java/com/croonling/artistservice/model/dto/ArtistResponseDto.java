package com.croonling.artistservice.model.dto;

import com.croonling.artistservice.model.entity.Artist;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@Getter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ArtistResponseDto {
    private String artistId;
    private List<String> artistNames;
    private List<String> genres;

    public static ArtistResponseDto fromEntity(Artist artist) {
        return ArtistResponseDto.builder()
                .artistId(artist.getArtistId())
                .artistNames(artist.getArtistNames())
                .genres(artist.getGenres())
                .build();
    }
}