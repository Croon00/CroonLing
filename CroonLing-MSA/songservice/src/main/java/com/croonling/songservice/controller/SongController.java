package com.croonling.songservice.controller;

import com.croonling.songservice.dto.SongResponseDto;
import com.croonling.songservice.service.SongService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/songs")
public class SongController {

    private final SongService songService;

    public SongController(SongService songService) {
        this.songService = songService;
    }

    @GetMapping("/{id}")
    public SongResponseDto getSong(@PathVariable String id) {
        return songService.getSongById(id);
    }
}
