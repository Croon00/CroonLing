package com.croonling.artistservice.controller;

import com.croonling.artistservice.model.dto.ArtistResponseDto;
import com.croonling.artistservice.service.ArtistService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/artists")
public class ArtistController {

    private final ArtistService artistServiceImpl;

    public ArtistController(ArtistService artistServiceImpl) {
        this.artistServiceImpl = artistServiceImpl;
    }

    // ✅ 아티스트 단건 조회
    @GetMapping("/{id}")
    public ResponseEntity<ArtistResponseDto> getArtistById(@PathVariable String id) {
        return ResponseEntity.ok(artistServiceImpl.getArtistById(id));
    }

    // ✅ 전체 아티스트 조회 (예시)
    @GetMapping
    public ResponseEntity<List<ArtistResponseDto>> getAllArtists() {
        return ResponseEntity.ok(artistServiceImpl.getAllArtists());
    }
}