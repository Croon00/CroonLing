package com.croonling.songservice.controller;

import com.croonling.songservice.model.dto.SongRequestDto;
import com.croonling.songservice.model.dto.SongResponseDto;
import com.croonling.songservice.service.SongService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/songs")
@RequiredArgsConstructor
public class SongController {

    private final SongService songService;


    // 노래 단건 조회
    @GetMapping("/{id}")
    public ResponseEntity<SongResponseDto> getSongById(@PathVariable String id) {
        return ResponseEntity.ok(songService.getSongById(id));
    }
}