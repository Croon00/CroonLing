"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllLyrics } from "@/api/lyrics";
import { getSongById } from "@/api/song";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Lyrics } from "@/types/Lyrics";
import { Song } from "@/types/Song";

type LyricsWithSongInfo = {
  lyrics: Lyrics;
  song: Song;
};

export default function LyricsPage() {
  const [items, setItems] = useState<LyricsWithSongInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLyricsWithSongs() {
      setLoading(true);
      try {
        const lyricsList = await getAllLyrics();
        const mapped = await Promise.all(
          lyricsList.map(async (lyrics) => ({
            lyrics,
            song: await getSongById(lyrics.songId),
          }))
        );
        setItems(mapped);
      } finally {
        setLoading(false);
      }
    }

    void fetchLyricsWithSongs();
  }, []);

  return (
    <SectionShell
      eyebrow="Lyrics"
      title="Original, translated, and phonetic lyric entries."
      description="Open lyric pages for a reading-focused layout with translation and pronunciation support."
    >
      {loading ? (
        <EmptyState
          title="Loading lyrics"
          description="Resolving lyric entries and related songs."
        />
      ) : items.length === 0 ? (
        <EmptyState
          title="No lyric entries found"
          description="The API did not return any lyric records."
        />
      ) : (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {items.map(({ lyrics, song }) => (
            <Link key={lyrics.songId} href={`/lyrics/${lyrics.songId}`}>
              <Card className="h-full transition-transform hover:-translate-y-1">
                <CardContent className="space-y-4">
                  <div className="flex items-center gap-4">
                    <div className="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-[1.25rem] border border-border bg-secondary">
                      {song.trackImageUrl ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img
                          src={song.trackImageUrl}
                          alt={song.songNames.join(", ")}
                          className="h-full w-full object-cover"
                        />
                      ) : (
                        <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
                          No cover
                        </span>
                      )}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xl font-semibold tracking-tight">
                        {song.songNames.join(", ")}
                      </p>
                      <p className="mt-2 text-sm text-muted-foreground">
                        {song.artistNames.join(", ")}
                      </p>
                    </div>
                  </div>
                  <p className="text-sm leading-6 text-muted-foreground">
                    {lyrics.translatedLyrics || lyrics.lyrics}
                  </p>
                  <div className="flex gap-2">
                    <Badge>Original</Badge>
                    {lyrics.translatedLyrics ? <Badge>Translated</Badge> : null}
                    {lyrics.phoneticsLyrics ? <Badge>Phonetics</Badge> : null}
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </SectionShell>
  );
}
