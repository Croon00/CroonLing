import * as React from "react";
import { cn } from "@/lib/utils";

export function Badge({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border border-border bg-secondary px-3 py-1 text-xs uppercase tracking-[0.2em] text-secondary-foreground",
        className
      )}
      {...props}
    />
  );
}
