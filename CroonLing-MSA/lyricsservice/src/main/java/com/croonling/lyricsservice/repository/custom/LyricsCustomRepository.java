package com.croonling.lyricsservice.repository.custom;

import com.croonling.lyricsservice.model.entity.Lyrics;

import java.util.List;

public interface LyricsCustomRepository {
    List<Lyrics> searchByKeyword(String keyword);
}
