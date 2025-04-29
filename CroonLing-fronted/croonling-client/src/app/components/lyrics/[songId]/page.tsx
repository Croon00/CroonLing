"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getLyricsBySongId } from "@/api/lyrics";
import { getSongById } from "@/api/song";
import { Lyrics } from "@/types/Lyrics";
import { Song } from "@/types/Song";

export default function LyricsDetailPage() {
  const { songId } = useParams();
  const [lyrics, setLyrics] = useState<Lyrics | null>(null);
  const [song, setSong] = useState<Song | null>(null);

  useEffect(() => {
    if (songId) {
      fetchData();
    }
  }, [songId]);

  const fetchData = async () => {
    const lyricsData = await getLyricsBySongId(songId as string);
    const songData = await getSongById(songId as string);
    setLyrics(lyricsData);
    setSong(songData);
  };

  if (!lyrics || !song) return <div>로딩 중...</div>;

  return (
    <div className="p-6">
      <div className="flex flex-col items-center mb-6">
        {song.trackImageUrl && (
          <img
            src={song.trackImageUrl}
            alt={`${song.songNames.join(", ")} 앨범 커버`}
            className="w-40 h-40 object-cover rounded-md mb-4"
          />
        )}
        <h1 className="text-2xl font-bold">{song.songNames.join(", ")}</h1>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">원본 가사</h2>
        <p className="whitespace-pre-line">{lyrics.lyrics}</p>
      </div>

      {lyrics.translatedLyrics && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-2">번역 가사</h2>
          <p className="whitespace-pre-line">{lyrics.translatedLyrics}</p>
        </div>
      )}

      {lyrics.phoneticsLyrics && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-2">발음</h2>
          <p className="whitespace-pre-line">{lyrics.phoneticsLyrics}</p>
        </div>
      )}

      {lyrics.phoneticsKoreanLyrics && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-2">한국어 표기 발음</h2>
          <p className="whitespace-pre-line">{lyrics.phoneticsKoreanLyrics}</p>
        </div>
      )}
    </div>
  );
}
