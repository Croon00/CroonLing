"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Artist } from "@/types/Artist";
import { getArtistById } from "@/api/artist"; // ✅ api 가져오기

export default function ArtistDetailPage() {
  const { artistId } = useParams();
  const [artist, setArtist] = useState<Artist | null>(null);

  useEffect(() => {
    if (artistId) {
      fetchArtist();
    }
  }, [artistId]);

  const fetchArtist = async () => {
    const data = await getArtistById(artistId as string);
    setArtist(data);
  };

  if (!artist) return <div>로딩 중...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        {artist.artistNames.join(", ")}
      </h1>
      <p>
        <strong>장르:</strong> {artist.genres.join(", ")}
      </p>
      <p>
        <strong>인기도:</strong> {artist.popularity}
      </p>
      <p>
        <strong>팔로워:</strong> {artist.followers}
      </p>
      {artist.profileImageUrl && (
        <div className="my-4">
          <img
            src={artist.profileImageUrl}
            alt="아티스트 프로필"
            className="w-64 h-64 object-cover"
          />
        </div>
      )}
      {artist.externalUrl && (
        <div className="mt-4">
          <a
            href={artist.externalUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            공식 페이지 이동
          </a>
        </div>
      )}
    </div>
  );
}
