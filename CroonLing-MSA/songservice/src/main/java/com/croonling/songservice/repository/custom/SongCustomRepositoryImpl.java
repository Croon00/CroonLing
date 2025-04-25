package com.croonling.songservice.repository.custom;

import com.croonling.songservice.model.entity.QSong;
import com.croonling.songservice.model.entity.Song;
import com.querydsl.jpa.impl.JPAQueryFactory;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class SongCustomRepositoryImpl implements SongCustomRepository {

    private final JPAQueryFactory queryFactory;

    public SongCustomRepositoryImpl(JPAQueryFactory queryFactory) {
        this.queryFactory = queryFactory;
    }

    @Override
    public List<Song> searchByTitle(String title) {
        QSong song = QSong.song;

        return queryFactory.selectFrom(song)
                .where(song.songNames.any().containsIgnoreCase(title)) // ✅ 핵심 부분
                .fetch();
    }
}
