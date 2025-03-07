package com.croonling.artistservice.model.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Entity
@Getter
@Setter
@Table(name = "artists")
public class Artist {
    @Id
    @Column(name = "artist_id", unique = true)
    private Long id;

    @Column(unique = true, nullable = false)
    private String artistId;

    @ElementCollection
    private List<String> artistNames;

    @ElementCollection
    private List<String> genres;

    private Integer popularity;
    private Integer followers;
    private String profileImageUrl;
    private String externalUrl;
}
