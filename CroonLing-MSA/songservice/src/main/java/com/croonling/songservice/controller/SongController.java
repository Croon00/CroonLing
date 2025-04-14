package com.croonling.songservice.controller;

import com.croonling.songservice.model.dto.SongRequestDto;
import com.croonling.songservice.model.dto.SongResponseDto;
import com.croonling.songservice.service.SongService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/songs")
@RequiredArgsConstructor
@Tag(name = "Song", description = "노래 관련 API") // ✅ 전체 컨트롤러 태그
public class SongController {

    private final SongService songService;


    // 노래 단건 조회
    @GetMapping("/{id}")
    @Operation(summary = "노래 단건 조회", description = "ID에 해당하는 노래 정보를 조회합니다.")
    public ResponseEntity<SongResponseDto> getSongById(@PathVariable String id) {
        return ResponseEntity.ok(songService.getSongById(id));
    }
}