package com.croonling.songservice.service;

import com.croonling.songservice.model.dto.SongRequestDto;
import com.croonling.songservice.model.dto.SongResponseDto;

import java.util.List;

public interface SongService {
    void saveFromKafka(SongRequestDto songRequestDto);
    SongResponseDto getSongById(String songId);
    List<SongResponseDto> getAllSongs();
}
