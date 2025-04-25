package com.croonling.artistservice.repository.custom;

import com.croonling.artistservice.model.entity.Artist;
import com.croonling.artistservice.model.entity.QArtist;
import com.querydsl.jpa.impl.JPAQueryFactory;
import jakarta.persistence.EntityManager;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class ArtistCustomRepositoryImpl implements ArtistCustomRepository{

    private final JPAQueryFactory queryFactory;

    public ArtistCustomRepositoryImpl(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    @Override
    public List<Artist> searchByName(String name) {
        QArtist artist = QArtist.artist;

        return queryFactory
                .selectFrom(artist)
                .where(artist.artistNames.any().containsIgnoreCase(name))
                .fetch();
    }
}
