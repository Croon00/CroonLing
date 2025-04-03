package com.croonling.artistservice.model.dto;

import lombok.*;

import java.util.List;

// dto/ArtistRequestDto.java
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ArtistRequestDto {
    private String artistId;
    private List<String> artistNames;
    private List<String> genres;
    private Integer popularity;
    private Integer followers;
    private String profileImageUrl;
    private String externalUrl;
}
