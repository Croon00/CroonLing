import Link from "next/link";

export default function MainPage() {
  return (
    <main className="mx-auto flex min-h-[calc(100vh-73px)] max-w-7xl flex-col justify-center px-6 py-16">
      <div className="grid gap-8 lg:grid-cols-[1.4fr_0.9fr]">
        <section className="rounded-[2rem] border border-foreground bg-foreground px-8 py-12 text-background shadow-soft">
          <p className="text-sm uppercase tracking-[0.4em] text-background/70">
            Song archive
          </p>
          <h1 className="mt-6 max-w-3xl text-5xl font-semibold tracking-tight sm:text-6xl">
            Songs, lyrics, and artists in one clean black and white interface.
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-7 text-background/72 sm:text-lg">
            Browse full track metadata, translated lyrics, phonetics, and artist
            profiles without visual clutter.
          </p>
          <div className="mt-10 flex flex-wrap gap-3">
            <Link
              href="/song"
              className="rounded-full bg-background px-5 py-3 text-sm font-medium text-foreground"
            >
              Explore songs
            </Link>
            <Link
              href="/lyrics"
              className="rounded-full border border-background/30 px-5 py-3 text-sm font-medium text-background"
            >
              Read lyrics
            </Link>
          </div>
        </section>

        <section className="grid gap-4">
          <div className="rounded-[2rem] border border-border bg-card p-6 shadow-soft">
            <p className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
              Sections
            </p>
            <div className="mt-6 grid gap-3">
              {[
                ["Songs", "Track list, album info, release dates"],
                ["Lyrics", "Original, translated, and phonetic views"],
                ["Artists", "Profiles, genres, popularity, followers"],
              ].map(([title, desc]) => (
                <div
                  key={title}
                  className="rounded-2xl border border-border bg-secondary px-4 py-4"
                >
                  <p className="font-medium">{title}</p>
                  <p className="mt-1 text-sm text-muted-foreground">{desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[2rem] border border-border bg-card p-6 shadow-soft">
            <p className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
              Design
            </p>
            <p className="mt-4 text-2xl font-semibold tracking-tight">
              Neutral palette, high contrast, dense information.
            </p>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              The UI is prepared for Tailwind and shadcn-style primitives with a
              single theme configuration.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}
