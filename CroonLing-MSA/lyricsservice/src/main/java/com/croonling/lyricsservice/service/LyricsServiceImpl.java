// LyricsServiceImpl.java
package com.croonling.lyricsservice.service;

import com.croonling.lyricsservice.model.dto.LyricsRequestDto;
import com.croonling.lyricsservice.model.dto.LyricsResponseDto;
import com.croonling.lyricsservice.model.entity.Lyrics;
import com.croonling.lyricsservice.repository.LyricsRepository;
import org.springframework.stereotype.Service;

@Service
public class LyricsServiceImpl implements LyricsService {

    private final LyricsRepository lyricsRepository;

    public LyricsServiceImpl(LyricsRepository lyricsRepository) {
        this.lyricsRepository = lyricsRepository;
    }

    @Override
    public void saveFromKafka(LyricsRequestDto dto) {
        Lyrics lyrics = Lyrics.builder()
                .songId(dto.getSongId())
                .lyrics(dto.getLyrics())
                .translatedLyrics(dto.getTranslatedLyrics())
                .phoneticsLyrics(dto.getPhoneticsLyrics())
                .phoneticsKoreanLyrics(dto.getPhoneticsKoreanLyrics())
                .kanjiInfo(dto.getKanjiInfo())
                .build();

        lyricsRepository.save(lyrics);
        System.out.println("📝 Lyrics 저장 완료: " + dto.getSongId());
    }

    @Override
    public LyricsResponseDto getLyricsBySongId(String songId) {
        Lyrics lyrics = lyricsRepository.findById(songId)
                .orElseThrow(() -> new RuntimeException("해당 가사가 없습니다. ID: " + songId));
        return LyricsResponseDto.fromEntity(lyrics);
    }


}