import Features from "./Features";
import Hero from "./Hero";
import { redirect } from "next/navigation";

export default function HomePage() {
  if (process.env.NEXT_PUBLIC_ENV === "local") {
    redirect("/upload");
  }

  return (
    <main className="">
      <Hero />
      <Features />
    </main>
  );
}
