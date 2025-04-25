// src/app/components/common/Navbar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const Navbar = () => {
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-zinc-900 text-white shadow-md">
      {/* 로고 */}
      <Link href="/" className="text-2xl font-extrabold text-teal-400">
        croonLing
      </Link>

      {/* 메뉴 */}
      <ul className="flex gap-6 text-lg font-medium">
        <li>
          <Link
            href="/artist"
            className={`hover:text-teal-400 ${
              isActive("/artist") ? "border-b-2 border-teal-400 pb-1" : ""
            }`}
          >
            아티스트
          </Link>
        </li>
        <li>
          <Link
            href="/song"
            className={`hover:text-teal-400 ${
              isActive("/song") ? "border-b-2 border-teal-400 pb-1" : ""
            }`}
          >
            노래
          </Link>
        </li>
        <li>
          <Link
            href="/lyrics"
            className={`hover:text-teal-400 ${
              isActive("/lyrics") ? "border-b-2 border-teal-400 pb-1" : ""
            }`}
          >
            가사
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
