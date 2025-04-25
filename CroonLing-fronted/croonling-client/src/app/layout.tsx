import "./globals.css";
import Navbar from "@/app/components/common/Navbar"; // ✅ Navbar import 추가

export const metadata = {
  title: "CroonLing",
  description: "AI 기반 가사 서비스",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased bg-zinc-950 text-white">
        <Navbar /> {/* ✅ 추가된 부분 */}
        {children}
      </body>
    </html>
  );
}
