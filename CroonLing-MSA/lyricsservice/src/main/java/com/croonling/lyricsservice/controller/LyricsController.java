// LyricsController.java
package com.croonling.lyricsservice.controller;

import com.croonling.lyricsservice.dto.LyricsResponseDto;
import com.croonling.lyricsservice.service.LyricsService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/lyrics")
public class LyricsController {

    private final LyricsService lyricsService;

    public LyricsController(LyricsService lyricsService) {
        this.lyricsService = lyricsService;
    }

    @GetMapping("/{songId}")
    public LyricsResponseDto getLyricsBySongId(@PathVariable String songId) {
        return lyricsService.getLyricsBySongId(songId);
    }
}