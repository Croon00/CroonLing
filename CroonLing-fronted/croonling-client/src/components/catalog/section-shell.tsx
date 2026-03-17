import { ReactNode } from "react";
import { Badge } from "@/components/ui/badge";

export function SectionShell({
  eyebrow,
  title,
  description,
  children,
}: {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <section className="rounded-[2rem] border border-border bg-card px-8 py-10 shadow-soft">
        <Badge>{eyebrow}</Badge>
        <h1 className="mt-6 text-4xl font-semibold tracking-tight sm:text-5xl">
          {title}
        </h1>
        <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground sm:text-base">
          {description}
        </p>
      </section>
      <div className="mt-8">{children}</div>
    </main>
  );
}
