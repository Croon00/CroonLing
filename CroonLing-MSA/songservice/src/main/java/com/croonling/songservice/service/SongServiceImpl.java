package com.croonling.songservice.service;

import com.croonling.songservice.model.dto.SongRequestDto;
import com.croonling.songservice.model.dto.SongResponseDto;
import com.croonling.songservice.model.entity.Song;
import com.croonling.songservice.repository.SongRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class SongServiceImpl implements SongService {

    private final SongRepository songRepository;

    public SongServiceImpl(SongRepository songRepository) {
        this.songRepository = songRepository;
    }

    @Override
    public void saveFromKafka(SongRequestDto songRequestDto) {
        Song song = Song.builder()
                .songId(songRequestDto.getSongId())
                .songNames(songRequestDto.getSongNames())
                .artistId(songRequestDto.getArtistId())
                .artistNames(songRequestDto.getArtistNames())
                .albumName(songRequestDto.getAlbumName())
                .releaseDate(songRequestDto.getReleaseDate())
                .trackImageUrl(songRequestDto.getTrackImageUrl())
                .url(songRequestDto.getUrl())
                .lyrics(songRequestDto.getLyrics())
                .translatedLyrics(songRequestDto.getTranslatedLyrics())
                .phoneticsLyrics(songRequestDto.getPhoneticsLyrics())
                .phoneticsKoreanLyrics(songRequestDto.getPhoneticsKoreanLyrics())
                .build();

        songRepository.save(song);
        System.out.println("🎵 Song 저장 완료: " + songRequestDto.getSongId());
    }

    @Override
    public SongResponseDto getSongById(String songId) {
        Song song = songRepository.findById(songId)
                .orElseThrow(() -> new RuntimeException("해당 곡이 없습니다. ID: " + songId));
        return SongResponseDto.fromEntity(song);
    }

    @Override
    public List<SongResponseDto> getAllSongs() {
        return songRepository.findAll()
                .stream()
                .map(SongResponseDto::fromEntity)
                .collect(Collectors.toList());
    }
}