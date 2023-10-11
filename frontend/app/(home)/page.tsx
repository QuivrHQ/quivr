"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToPreviousPageOrChatPage } from "@/lib/helpers/redirectToPreviousPageOrChatPage";

import Features from "./Features";
import Hero from "./Hero";
import { HomeHeader } from "./components";

const HomePage = (): JSX.Element => {
  const { session } = useSupabase();

  useEffect(() => {
    if (session?.user !== undefined) {
      redirectToPreviousPageOrChatPage();
    }
  }, [session?.user]);

  const isNewHomePage = useFeatureIsOn("new-homepage-activated");

  if (isNewHomePage) {
    return (
      <>
        <div data-testid="home-page">
          <div className="fixed bg-gradient-to-b from-[#6300FF] to-[#D07DF9] w-screen h-[50vh] z-[-1]"></div>
          <HomeHeader />
          <main>
            <div className="mx-auto my-5 p-5 w-min-content bg-yellow-100 rounded-lg">
              🚧 New homepage in progress 🚧
            </div>
          </main>
        </div>
      </>
    );
  } else {
    return (
      <main data-testid="home-page">
        <Hero />
        <Features />
      </main>
    );
  }
};

export default HomePage;
