package com.croonling.artistservice.repository;

import com.croonling.artistservice.model.entity.Artist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface AritstRepository extends JpaRepository<Artist, Long> {
    Artist frindByArtistId(String artistId);

}
