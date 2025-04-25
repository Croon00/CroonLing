package com.croonling.artistservice.repository.custom;

import com.croonling.artistservice.model.entity.Artist;

import javax.swing.*;
import java.util.List;

public interface ArtistCustomRepository {
    List<Artist> searchByName(String name);
}
