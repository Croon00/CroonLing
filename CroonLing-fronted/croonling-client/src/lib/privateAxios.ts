import { Artist, ArtistListItem } from "@/types/Artist";
import publicAxios from "@/lib/publicAxios";

export const getAllArtists = async (): Promise<ArtistListItem[]> => {
  const res = await publicAxios.get("/api/artist");
  return res.data;
};

export const searchArtistsByName = async (
  name: string
): Promise<ArtistListItem[]> => {
  const res = await publicAxios.get(
    `/api/artist/search?name=${encodeURIComponent(name)}`
  );
  return res.data;
};

export const getArtistById = async (artistId: string): Promise<Artist> => {
  const res = await publicAxios.get(`/api/artist/${artistId}`);
  return res.data;
};
