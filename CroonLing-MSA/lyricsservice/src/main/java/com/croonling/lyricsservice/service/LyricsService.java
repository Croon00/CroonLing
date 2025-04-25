package com.croonling.lyricsservice.service;

import com.croonling.lyricsservice.model.dto.LyricsRequestDto;
import com.croonling.lyricsservice.model.dto.LyricsResponseDto;

public interface LyricsService {
    void saveFromKafka(LyricsRequestDto dto);
    public LyricsResponseDto getLyricsBySongId(String songId);
}
