package com.croonling.artistservice.service;

import com.croonling.artistservice.model.dto.ArtistRequestDto;
import com.croonling.artistservice.model.dto.ArtistResponseDto;
import com.croonling.artistservice.model.entity.Artist;
import com.croonling.artistservice.repository.ArtistRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ArtistServiceImpl implements ArtistService{

    private ArtistRepository artistRepository;


    public ArtistServiceImpl(ArtistRepository artistRepository) {
        this.artistRepository = artistRepository;
    }

    @Override
    public void saveFromKafka(ArtistRequestDto artistRequestDto) {
        Artist artist = Artist.builder()
                .artistId(artistRequestDto.getArtistId())
                .artistNames(artistRequestDto.getArtistNames())
                .genres(artistRequestDto.getGenres())
                .popularity(artistRequestDto.getPopularity())
                .followers(artistRequestDto.getFollowers())
                .profileImageUrl(artistRequestDto.getProfileImageUrl())
                .externalUrl(artistRequestDto.getExternalUrl())
                .build();

        artistRepository.save(artist);
    }

    @Override
    public ArtistResponseDto getArtistById(String id) {
        Artist artist = artistRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("해당 아티스트가 없습니다."));
        return ArtistResponseDto.fromEntity(artist);
    }

    @Override
    public List<ArtistResponseDto> getAllArtists() {
        return artistRepository.findAll()
                .stream()
                .map(ArtistResponseDto::fromEntity)
                .collect(Collectors.toList());
    }
}
