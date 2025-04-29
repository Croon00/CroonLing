// src/api/lyrics.ts
import publicAxios from "@/lib/publicAxios";
import { Lyrics } from "@/types/Lyrics";

export const getAllLyrics = async (): Promise<Lyrics[]> => {
  const res = await publicAxios.get("/api/lyrics");
  return res.data;
};

export const searchLyricsByKeyword = async (
  keyword: string
): Promise<Lyrics[]> => {
  const res = await publicAxios.get(
    `/api/lyrics/search?keyword=${encodeURIComponent(keyword)}`
  );
  return res.data;
};

export const getLyricsBySongId = async (songId: string): Promise<Lyrics> => {
  const res = await publicAxios.get(`/api/lyrics/${songId}`);
  return res.data;
};
