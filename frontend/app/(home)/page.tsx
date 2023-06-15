import { redirect } from "next/navigation";

import Features from "./Features";
import Hero from "./Hero";

const HomePage = (): JSX.Element => {
  if (process.env.NEXT_PUBLIC_ENV === "local") {
    redirect("/upload");
  }

  return (
    <main className="">
      <Hero />
      <Features />
    </main>
  );
};

export default HomePage;
