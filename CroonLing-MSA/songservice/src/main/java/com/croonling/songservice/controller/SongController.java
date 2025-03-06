package com.croonling.songservice.controller;

import com.croonling.songservice.dto.SongRequestDto;
import com.croonling.songservice.dto.SongResponseDto;
import com.croonling.songservice.service.SongService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/songs")
@RequiredArgsConstructor
public class SongController {

    private final SongService songService;

    @PostMapping
    public ResponseEntity<SongResponseDto> saveSong(@RequestBody SongRequestDto requestDto) {
        return ResponseEntity.ok(songService.saveSong(requestDto));
    }

    @GetMapping("/{id}")
    public ResponseEntity<SongResponseDto> getSongById(@PathVariable String id) {
        return ResponseEntity.ok(songService.getSongById(id));
    }
}
