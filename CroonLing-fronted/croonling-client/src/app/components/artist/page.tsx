"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArtistListItem } from "@/types/Artist";
import { getAllArtists, searchArtistsByName } from "@/api/artist";

export default function ArtistPage() {
  const [artists, setArtists] = useState<ArtistListItem[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchArtists();
  }, []);

  const fetchArtists = async () => {
    const data = await getAllArtists();
    setArtists(data);
  };

  const handleSearch = async () => {
    if (search.trim() === "") {
      fetchArtists();
      return;
    }
    const data = await searchArtistsByName(search);
    setArtists(data);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">🎤 아티스트 목록</h1>

      {/* 검색창 */}
      <div className="flex mb-6">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="아티스트 이름 검색"
          className="border p-2 w-full rounded-l"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-500 text-white px-4 py-2 rounded-r"
        >
          검색
        </button>
      </div>

      {/* 카드 리스트 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {artists.map((artist) => (
          <Link
            key={artist.artistId}
            href={`/artist/${artist.artistId}`}
            className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-300 p-4 text-center"
          >
            {artist.profileImageUrl && (
              <img
                src={artist.profileImageUrl}
                alt={`${artist.artistNames.join(", ")} 프로필`}
                className="w-24 h-24 object-cover rounded-full mx-auto mb-4"
              />
            )}
            <h2 className="text-lg font-semibold text-gray-800">
              {artist.artistNames.join(", ")}
            </h2>
            <p className="text-sm text-gray-500">{artist.genres.join(", ")}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
