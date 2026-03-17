"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllSongs, searchSongsByTitle } from "@/api/song";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Input } from "@/components/ui/input";
import { Song } from "@/types/Song";

export default function SongPage() {
  const [songs, setSongs] = useState<Song[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void fetchSongs();
  }, []);

  async function fetchSongs() {
    setLoading(true);
    try {
      setSongs(await getAllSongs());
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch() {
    setLoading(true);
    try {
      setSongs(
        search.trim() ? await searchSongsByTitle(search) : await getAllSongs()
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <SectionShell
      eyebrow="Songs"
      title="Track list with album and artist context."
      description="Search by title, scan artwork, and jump into detailed song metadata."
    >
      <div className="mb-6 flex flex-col gap-3 rounded-[1.5rem] border border-border bg-card p-4 shadow-soft sm:flex-row">
        <Input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              void handleSearch();
            }
          }}
          placeholder="Search songs"
        />
        <Button onClick={() => void handleSearch()} className="sm:min-w-36">
          Search
        </Button>
      </div>

      {loading ? (
        <EmptyState
          title="Loading songs"
          description="Fetching song data from the API."
        />
      ) : songs.length === 0 ? (
        <EmptyState
          title="No songs found"
          description="Try a different title keyword."
        />
      ) : (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {songs.map((song) => (
            <Link key={song.songId} href={`/song/${song.songId}`}>
              <Card className="h-full transition-transform hover:-translate-y-1">
                <CardContent className="flex h-full gap-4">
                  <div className="flex h-28 w-28 shrink-0 items-center justify-center overflow-hidden rounded-[1.25rem] border border-border bg-secondary">
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
                  <div className="min-w-0 flex-1">
                    <p className="text-xl font-semibold tracking-tight">
                      {song.songNames.join(", ")}
                    </p>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {song.artistNames.join(", ")}
                    </p>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {song.albumName || "Album information unavailable"}
                    </p>
                    <div className="mt-4">
                      <Badge>{song.releaseDate || "Release date unknown"}</Badge>
                    </div>
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
