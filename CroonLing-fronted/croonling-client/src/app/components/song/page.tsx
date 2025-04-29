"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllSongs, searchSongsByTitle } from "@/api/song";
import { SongListItem } from "@/types/Song";

export default function SongPage() {
  const [songs, setSongs] = useState<SongListItem[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchSongs();
  }, []);

  const fetchSongs = async () => {
    const data = await getAllSongs();
    setSongs(data);
  };

  const handleSearch = async () => {
    if (search.trim() === "") {
      fetchSongs();
      return;
    }
    const data = await searchSongsByTitle(search);
    setSongs(data);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">🎵 곡 목록</h1>

      {/* 검색창 */}
      <div className="flex mb-6">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="곡 제목 검색"
          className="border p-2 w-full rounded-l"
        />
        <button
          onClick={handleSearch}
          className="bg-green-500 text-white px-4 py-2 rounded-r"
        >
          검색
        </button>
      </div>

      {/* 카드 리스트 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {songs.map((song) => (
          <Link
            key={song.songId}
            href={`/song/${song.songId}`}
            className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-300 p-4 text-center"
          >
            {song.trackImageUrl && (
              <img
                src={song.trackImageUrl}
                alt={`${song.songNames.join(", ")} 앨범 커버`}
                className="w-32 h-32 object-cover rounded-md mx-auto mb-4"
              />
            )}
            <h2 className="text-md font-semibold text-gray-800">
              {song.songNames.join(", ")}
            </h2>
          </Link>
        ))}
      </div>
    </div>
  );
}
