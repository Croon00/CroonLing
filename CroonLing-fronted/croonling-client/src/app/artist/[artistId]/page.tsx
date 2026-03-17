"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { getArtistById } from "@/api/artist";
import { SectionShell } from "@/components/catalog/section-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Artist } from "@/types/Artist";

export default function ArtistDetailPage() {
  const params = useParams<{ artistId: string }>();
  const [artist, setArtist] = useState<Artist | null>(null);

  useEffect(() => {
    if (!params.artistId) {
      return;
    }

    void getArtistById(params.artistId).then(setArtist);
  }, [params.artistId]);

  return (
    <SectionShell
      eyebrow="Artist detail"
      title={artist ? artist.artistNames.join(", ") : "Loading artist"}
      description="A focused view for genres, audience scale, and external profile links."
    >
      {!artist ? (
        <EmptyState
          title="Loading artist"
          description="The artist profile is being retrieved."
        />
      ) : (
        <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <Card>
            <CardContent className="space-y-6">
              <div className="flex aspect-square items-center justify-center overflow-hidden rounded-[1.5rem] border border-border bg-secondary">
                {artist.profileImageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={artist.profileImageUrl}
                    alt={artist.artistNames.join(", ")}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <span className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
                    No image
                  </span>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {artist.genres.map((genre) => (
                  <Badge key={genre}>{genre}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-[1.25rem] border border-border bg-secondary p-5">
                  <p className="text-sm text-muted-foreground">Popularity</p>
                  <p className="mt-2 text-3xl font-semibold">{artist.popularity}</p>
                </div>
                <div className="rounded-[1.25rem] border border-border bg-secondary p-5">
                  <p className="text-sm text-muted-foreground">Followers</p>
                  <p className="mt-2 text-3xl font-semibold">
                    {artist.followers.toLocaleString()}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-sm uppercase tracking-[0.25em] text-muted-foreground">
                  Names
                </p>
                <p className="mt-3 text-lg leading-8">{artist.artistNames.join(", ")}</p>
              </div>
              <div className="flex flex-wrap gap-3">
                <Link href="/artist">
                  <Button variant="outline">Back to artists</Button>
                </Link>
                {artist.externalUrl ? (
                  <a href={artist.externalUrl} target="_blank" rel="noreferrer">
                    <Button>Open external profile</Button>
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
