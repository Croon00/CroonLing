package com.croonling.lyricsservice.repository;

import com.croonling.lyricsservice.entity.Lyrics;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LyricsRepository extends JpaRepository<Lyrics, String> {
}
