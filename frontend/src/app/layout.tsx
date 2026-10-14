import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import { Navbar } from "@/components/layout/navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Meeting Assistant Agent | MoM, Tasks & Semantic Search",
  description:
    "Production-ready AI meeting assistant combining Whisper speech-to-text, Gemini 2.5 Flash, LangGraph workflow pipelines, and FAISS RAG semantic retrieval.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-zinc-950 text-zinc-100 antialiased`}>
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
            <footer className="border-t border-zinc-800/80 py-6 text-center text-xs text-zinc-400">
              AI Meeting Assistant Agent &bull; Hackathon Edition &bull; Clean Architecture &bull; Next.js 15 &bull; FastAPI
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}
