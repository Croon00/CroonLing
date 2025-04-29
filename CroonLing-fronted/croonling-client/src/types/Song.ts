// src/types/Song.ts
export interface Song {
  songId: string;
  songNames: string[];
  artistId: string;
  artistNames: string[];
  albumName: string;
  releaseDate: string;
  trackImageUrl: string;
  url: string;
  lyrics: string;
  translatedLyrics: string;
  phoneticsLyrics: string;
  phoneticsKoreanLyrics: string;
}

export type SongListItem = Pick<Song, "songId" | "songNames" | "trackImageUrl">;
