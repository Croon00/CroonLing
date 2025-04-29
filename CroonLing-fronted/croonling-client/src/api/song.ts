// src/api/song.ts
import publicAxios from "@/lib/publicAxios";
import { Song } from "@/types/Song";

export const getAllSongs = async (): Promise<Song[]> => {
  const res = await publicAxios.get("/api/song");
  return res.data;
};

export const searchSongsByTitle = async (title: string): Promise<Song[]> => {
  const res = await publicAxios.get(
    `/api/song/search?title=${encodeURIComponent(title)}`
  );
  return res.data;
};

export const getSongById = async (songId: string): Promise<Song> => {
  const res = await publicAxios.get(`/api/song/${songId}`);
  return res.data;
};
