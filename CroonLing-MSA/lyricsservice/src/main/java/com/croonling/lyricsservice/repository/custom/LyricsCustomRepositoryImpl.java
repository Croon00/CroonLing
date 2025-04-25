package com.croonling.lyricsservice.repository.custom;

import com.croonling.lyricsservice.model.entity.Lyrics;
import com.croonling.lyricsservice.model.entity.QLyrics;
import com.querydsl.jpa.impl.JPAQueryFactory;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class LyricsCustomRepositoryImpl implements LyricsCustomRepository {

    private final JPAQueryFactory queryFactory;

    public LyricsCustomRepositoryImpl(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    @Override
    public List<Lyrics> searchByKeyword(String keyword) {
        QLyrics lyrics = QLyrics.lyrics1;

        return queryFactory.selectFrom(lyrics)
                .where(lyrics.lyrics.containsIgnoreCase(keyword))
                .fetch();
    }
}
