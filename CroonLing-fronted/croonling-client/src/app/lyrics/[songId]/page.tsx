"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { getLyricsBySongId } from "@/api/lyrics";
import { getSongById } from "@/api/song";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Separator } from "@/components/ui/separator";
import { Lyrics } from "@/types/Lyrics";
import { Song } from "@/types/Song";

export default function LyricsDetailPage() {
  const params = useParams<{ songId: string }>();
  const [lyrics, setLyrics] = useState<Lyrics | null>(null);
  const [song, setSong] = useState<Song | null>(null);

  useEffect(() => {
    if (!params.songId) {
      return;
    }

    async function fetchData() {
      const [lyricsData, songData] = await Promise.all([
        getLyricsBySongId(params.songId),
        getSongById(params.songId),
      ]);
      setLyrics(lyricsData);
      setSong(songData);
    }

    void fetchData();
  }, [params.songId]);

  return (
    <SectionShell
      eyebrow="Lyrics detail"
      title={song ? song.songNames.join(", ") : "Loading lyrics"}
      description="Read the original lyric text together with translation and pronunciation guidance."
    >
      {!lyrics || !song ? (
        <EmptyState
          title="Loading lyrics"
          description="The lyric detail is being retrieved."
        />
      ) : (
        <div className="grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
          <Card>
            <CardContent className="space-y-6">
              <div className="flex aspect-square items-center justify-center overflow-hidden rounded-[1.5rem] border border-border bg-secondary">
                {song.trackImageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={song.trackImageUrl}
                    alt={song.songNames.join(", ")}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <span className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
                    No cover
                  </span>
                )}
              </div>
              <div>
                <p className="text-2xl font-semibold tracking-tight">
                  {song.songNames.join(", ")}
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  {song.artistNames.join(", ")}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge>Original</Badge>
                {lyrics.translatedLyrics ? <Badge>Translated</Badge> : null}
                {lyrics.phoneticsLyrics ? <Badge>Phonetics</Badge> : null}
                {lyrics.phoneticsKoreanLyrics ? <Badge>Korean phonetics</Badge> : null}
              </div>
              <div className="flex flex-wrap gap-3">
                <Link href={`/song/${song.songId}`}>
                  <Button>View song detail</Button>
                </Link>
                <Link href="/lyrics">
                  <Button variant="outline">Back to lyrics</Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="space-y-6">
              <section>
                <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                  Original lyrics
                </p>
                <p className="mt-4 whitespace-pre-line text-sm leading-7 sm:text-base">
                  {lyrics.lyrics}
                </p>
              </section>

              {lyrics.translatedLyrics ? (
                <>
                  <Separator />
                  <section>
                    <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                      Translated lyrics
                    </p>
                    <p className="mt-4 whitespace-pre-line text-sm leading-7 sm:text-base">
                      {lyrics.translatedLyrics}
                    </p>
                  </section>
                </>
              ) : null}

              {lyrics.phoneticsLyrics ? (
                <>
                  <Separator />
                  <section>
                    <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                      Phonetics
                    </p>
                    <p className="mt-4 whitespace-pre-line text-sm leading-7 sm:text-base">
                      {lyrics.phoneticsLyrics}
                    </p>
                  </section>
                </>
              ) : null}

              {lyrics.phoneticsKoreanLyrics ? (
                <>
                  <Separator />
                  <section>
                    <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                      Korean phonetics
                    </p>
                    <p className="mt-4 whitespace-pre-line text-sm leading-7 sm:text-base">
                      {lyrics.phoneticsKoreanLyrics}
                    </p>
                  </section>
                </>
              ) : null}
            </CardContent>
          </Card>
        </div>
      )}
    </SectionShell>
  );
}
