package com.croonling.lyricsservice.service;

import com.croonling.lyricsservice.dto.LyricsRequestDto;
import com.croonling.lyricsservice.dto.LyricsResponseDto;

public interface LyricsService {
    void saveFromKafka(LyricsRequestDto dto);
    public LyricsResponseDto getLyricsBySongId(String songId);
}
