package com.croonling.artistservice.model.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@Getter
@Setter
@Table(name = "artists")
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Artist {
    @Id
    @Column(name = "artist_id", unique = true)
    private String artistId;

    @ElementCollection
    @CollectionTable(name = "artist_names", joinColumns = @JoinColumn(name = "artist_id"))
    @Column(name = "name")
    private List<String> artistNames;

    @ElementCollection
    @CollectionTable(name = "artist_genres", joinColumns = @JoinColumn(name = "artist_id"))
    @Column(name = "genre")
    private List<String> genres;

    private Integer popularity;
    private Integer followers;
    private String profileImageUrl;
    private String externalUrl;
}
