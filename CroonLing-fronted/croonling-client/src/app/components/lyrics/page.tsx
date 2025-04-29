"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Lyrics } from "@/types/Lyrics";
import { Song } from "@/types/Song";
import { getAllLyrics } from "@/api/lyrics";
import { getSongById } from "@/api/song";

interface LyricsWithSongInfo {
  lyrics: Lyrics;
  song: Song;
}

export default function LyricsPage() {
  const [lyricsWithSongs, setLyricsWithSongs] = useState<LyricsWithSongInfo[]>(
    []
  );

  useEffect(() => {
    fetchLyricsWithSongs();
  }, []);

  const fetchLyricsWithSongs = async () => {
    const lyricsList = await getAllLyrics();

    const lyricsWithSongsData = await Promise.all(
      lyricsList.map(async (lyrics) => {
        const song = await getSongById(lyrics.songId);
        return { lyrics, song };
      })
    );

    setLyricsWithSongs(lyricsWithSongsData);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">📝 가사 목록</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {lyricsWithSongs.map(({ lyrics, song }) => (
          <Link
            key={lyrics.songId}
            href={`/lyrics/${lyrics.songId}`}
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
