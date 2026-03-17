"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllArtists, searchArtistsByName } from "@/api/artist";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Input } from "@/components/ui/input";
import { ArtistListItem } from "@/types/Artist";

export default function ArtistPage() {
  const [artists, setArtists] = useState<ArtistListItem[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void fetchArtists();
  }, []);

  async function fetchArtists() {
    setLoading(true);
    try {
      setArtists(await getAllArtists());
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch() {
    setLoading(true);
    try {
      setArtists(
        search.trim() ? await searchArtistsByName(search) : await getAllArtists()
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <SectionShell
      eyebrow="Artists"
      title="Browse artist profiles and genres."
      description="Search artist names, open profile details, and review popularity and follower metrics in a restrained monochrome layout."
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
          placeholder="Search artists"
        />
        <Button onClick={() => void handleSearch()} className="sm:min-w-36">
          Search
        </Button>
      </div>

      {loading ? (
        <EmptyState
          title="Loading artists"
          description="Fetching artist data from the API."
        />
      ) : artists.length === 0 ? (
        <EmptyState
          title="No artists found"
          description="Try a different keyword or clear the search field."
        />
      ) : (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {artists.map((artist) => (
            <Link key={artist.artistId} href={`/artist/${artist.artistId}`}>
              <Card className="h-full transition-transform hover:-translate-y-1">
                <CardContent className="flex h-full gap-4">
                  <div className="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-[1.25rem] border border-border bg-secondary">
                    {artist.profileImageUrl ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={artist.profileImageUrl}
                        alt={artist.artistNames.join(", ")}
                        className="h-full w-full object-cover"
                      />
                    ) : (
                      <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
                        No image
                      </span>
                    )}
                  </div>
                  <div className="flex min-w-0 flex-1 flex-col justify-between">
                    <div>
                      <p className="text-xl font-semibold tracking-tight">
                        {artist.artistNames.join(", ")}
                      </p>
                      <p className="mt-2 text-sm text-muted-foreground">
                        Popularity {artist.popularity}
                      </p>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {artist.genres.slice(0, 3).map((genre) => (
                        <Badge key={genre}>{genre}</Badge>
                      ))}
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
