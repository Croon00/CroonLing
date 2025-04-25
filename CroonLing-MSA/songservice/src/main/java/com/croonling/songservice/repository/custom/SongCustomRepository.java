package com.croonling.songservice.repository.custom;

import com.croonling.songservice.model.entity.Song;

import java.util.List;

public interface SongCustomRepository {
    List<Song> searchByTitle(String title);
}
