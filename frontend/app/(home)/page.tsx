"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToPreviousPageOrChatPage } from "@/lib/helpers/redirectToPreviousPageOrChatPage";

import Features from "./Features";
import Hero from "./Hero";
import {
  DemoSection,
  ExampleSection,
  FooterSection,
  HomeHeader,
  HomeSection,
  IntroSection,
  SecuritySection,
  TestimonialsSection,
} from "./components";

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
        <div data-testid="home-page" className="relative">
          <HomeHeader />

          <main className="relative flex flex-col items-center z-[-1]">
            <HomeSection bg="transparent">
              <IntroSection />
            </HomeSection>

            <HomeSection
              bg="bg-[#FCFAF6]"
              slantAfter="down"
              hiddenOnMobile={true}
            >
              <DemoSection />
            </HomeSection>

            <HomeSection bg="bg-[#362469]" slantCurrent="down">
              <ExampleSection />
            </HomeSection>

            <HomeSection bg="bg-white" slantBefore="down" slantAfter="up">
              <SecuritySection />
            </HomeSection>

            <HomeSection bg="bg-[#FCFAF6]" slantCurrent="up">
              <TestimonialsSection />
            </HomeSection>

            <HomeSection
              bg="bg-gradient-to-b from-[#7A27FD] to-[#D07DF9]"
              slantBefore="up"
            >
              <FooterSection />
            </HomeSection>
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
