"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { getSongById } from "@/api/song";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Song } from "@/types/Song";

export default function SongDetailPage() {
  const params = useParams<{ songId: string }>();
  const [song, setSong] = useState<Song | null>(null);

  useEffect(() => {
    if (!params.songId) {
      return;
    }

    void getSongById(params.songId).then(setSong);
  }, [params.songId]);

  return (
    <SectionShell
      eyebrow="Song detail"
      title={song ? song.songNames.join(", ") : "Loading song"}
      description="Album context, artist credits, and direct links in a compact editorial layout."
    >
      {!song ? (
        <EmptyState
          title="Loading song"
          description="The track detail is being retrieved."
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
              <div className="flex flex-wrap gap-2">
                <Badge>{song.releaseDate || "Unknown date"}</Badge>
                {song.albumName ? <Badge>{song.albumName}</Badge> : null}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="space-y-6">
              <div>
                <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                  Artists
                </p>
                <p className="mt-3 text-lg leading-8">{song.artistNames.join(", ")}</p>
              </div>
              <div>
                <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                  Album
                </p>
                <p className="mt-3 text-lg leading-8">
                  {song.albumName || "Album information unavailable"}
                </p>
              </div>
              <div>
                <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                  Metadata
                </p>
                <div className="mt-3 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-[1.25rem] border border-border bg-secondary p-5">
                    <p className="text-sm text-muted-foreground">Song ID</p>
                    <p className="mt-2 break-all text-sm font-medium">{song.songId}</p>
                  </div>
                  <div className="rounded-[1.25rem] border border-border bg-secondary p-5">
                    <p className="text-sm text-muted-foreground">Artist ID</p>
                    <p className="mt-2 break-all text-sm font-medium">{song.artistId}</p>
                  </div>
                </div>
              </div>
              <div className="flex flex-wrap gap-3">
                <Link href={`/lyrics/${song.songId}`}>
                  <Button>View lyrics</Button>
                </Link>
                <Link href="/song">
                  <Button variant="outline">Back to songs</Button>
                </Link>
                {song.url ? (
                  <a href={song.url} target="_blank" rel="noreferrer">
                    <Button variant="ghost">Open external link</Button>
                  </a>
                ) : null}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </SectionShell>
  );
}
