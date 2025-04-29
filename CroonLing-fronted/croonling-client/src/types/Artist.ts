// src/types/Artist.ts
export interface Artist {
  artistId: string;
  artistNames: string[];
  genres: string[];
  popularity: number;
  followers: number;
  profileImageUrl: string;
  externalUrl: string;
}

export type ArtistListItem = Pick<
  Artist,
  "artistId" | "artistNames" | "genres" | "popularity" | "profileImageUrl"
>;
