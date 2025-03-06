package com.croonling.songservice.service;

import com.croonling.songservice.dto.SongRequestDto;
import com.croonling.songservice.dto.SongResponseDto;

public interface SongService {
    SongResponseDto saveSong(SongRequestDto requestDto);
    SongResponseDto getSongById(String songId);
}
