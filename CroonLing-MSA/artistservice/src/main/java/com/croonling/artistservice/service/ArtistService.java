package com.croonling.artistservice.service;

import com.croonling.artistservice.model.dto.ArtistRequestDto;
import com.croonling.artistservice.model.dto.ArtistResponseDto;

import java.util.List;

public interface ArtistService
{
    void saveFromKafka(ArtistRequestDto artistRequestDto);
    ArtistResponseDto getArtistById(String id);
    List<ArtistResponseDto> getAllArtists();
}
