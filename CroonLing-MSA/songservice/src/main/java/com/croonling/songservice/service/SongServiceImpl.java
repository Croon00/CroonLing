package com.croonling.songservice.service;

import com.croonling.songservice.converter.SongConverter;
import com.croonling.songservice.dto.SongRequestDto;
import com.croonling.songservice.dto.SongResponseDto;
import com.croonling.songservice.entity.Song;
import com.croonling.songservice.exception.SongNotFoundException;
import com.croonling.songservice.repository.SongRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class SongServiceImpl implements SongService {

    private final SongRepository songRepository;
    private final SongConverter songConverter;

    @Override
    @Transactional
    public SongResponseDto saveSong(SongRequestDto songRequestDto) {
        Song song = songConverter.toEntity(songRequestDto);
        Song savedSong = songRepository.save(song);
        return songConverter.toResponse(savedSong);
    }

    @Override
    @Transactional(readOnly = true)
    public SongResponseDto getSongById(String songId) {
        Song song = songRepository.findById(songId)
                .orElseThrow(() -> new SongNotFoundException("해당 곡을 찾을 수 없습니다. ID: " + songId));
        return songConverter.toResponse(song);
    }
}
