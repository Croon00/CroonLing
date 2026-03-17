"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const links = [
  { href: "/", label: "Home" },
  { href: "/song", label: "Songs" },
  { href: "/lyrics", label: "Lyrics" },
  { href: "/artist", label: "Artists" },
];

export default function Navbar() {
  const pathname = usePathname();

  const isActive = (path: string) =>
    path === "/" ? pathname === path : pathname.startsWith(path);

  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-background/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full border border-foreground bg-foreground text-background">
            CL
          </div>
          <div>
            <p className="text-lg font-semibold tracking-tight">CroonLing</p>
            <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
              monochrome library
            </p>
          </div>
        </Link>

        <nav className="flex items-center gap-2 rounded-full border border-border bg-background/90 p-1">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "rounded-full px-4 py-2 text-sm text-muted-foreground",
                "hover:bg-foreground hover:text-background",
                isActive(link.href) && "bg-foreground text-background"
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
