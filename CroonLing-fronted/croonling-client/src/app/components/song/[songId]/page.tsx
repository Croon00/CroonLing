"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getSongById } from "@/api/song";
import { Song } from "@/types/Song";

export default function SongDetailPage() {
  const { songId } = useParams();
  const [song, setSong] = useState<Song | null>(null);

  useEffect(() => {
    if (songId) {
      fetchSong();
    }
  }, [songId]);

  const fetchSong = async () => {
    const data = await getSongById(songId as string);
    setSong(data);
  };

  if (!song) return <div>로딩 중...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">{song.songNames.join(", ")}</h1>
      <p>
        <strong>아티스트:</strong> {song.artistNames.join(", ")}
      </p>
      <p>
        <strong>앨범:</strong> {song.albumName}
      </p>
      <p>
        <strong>발매일:</strong> {song.releaseDate}
      </p>

      {song.trackImageUrl && (
        <div className="my-4">
          <img
            src={song.trackImageUrl}
            alt="앨범 커버"
            className="w-64 h-64 object-cover"
          />
        </div>
      )}

      {song.url && (
        <a
          href={song.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:underline"
        >
          공식 링크 이동
        </a>
      )}
    </div>
  );
}
