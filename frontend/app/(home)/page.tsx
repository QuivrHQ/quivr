import Link from "next/link";
import Hero from "./Hero";
import { Analytics } from '@vercel/analytics/react';

export default function HomePage() {
  return (
    <main className="">
      <Hero />
      <Analytics />
    </main>
  );
}
