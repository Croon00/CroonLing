import "./globals.css";
import Navbar from "@/app/components/common/Navbar";

export const metadata = {
  title: "CroonLing",
  description: "Browse songs, lyrics, and artists in a refined monochrome UI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>
        <div className="min-h-screen">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
