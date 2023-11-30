"use client";
import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToPreviousPageOrChatPage } from "@/lib/helpers/redirectToPreviousPageOrChatPage";

import {
  FooterSection,
  HomeHeader,
  HomeSection,
  IntroSection,
} from "./components";

const HomePage = (): JSX.Element => {
  const { session } = useSupabase();

  useEffect(() => {
    if (session?.user !== undefined) {
      redirectToPreviousPageOrChatPage();
    }
  }, [session?.user]);

  return (
    <>
      {/* <HomeHeaderBackground /> */}
      <HomeHeader />

      <main
        className="relative flex flex-col items-center h-full"
        data-testid="home-page"
      >
        <HomeSection bg="transparent">
          <IntroSection />
        </HomeSection>

        {/* <HomeSection bg="bg-[#FCFAF6]" slantAfter="down" hiddenOnMobile={true}>
          <DemoSection />
        </HomeSection> */}

        {/* <HomeSection
          bg="bg-[#362469]"

          gradient="bg-gradient-to-t bg-gradient-to-t from-white to-[#362469]"
        >
          <UseCases />
          <div />
        </HomeSection> */}

        {/* <HomeSection bg="bg-white" slantBefore="down" slantAfter="up">
          <SecuritySection />
        </HomeSection> */}

        {/* <HomeSection bg="bg-[#FCFAF6]" slantCurrent="up">
          <TestimonialsSection />
        </HomeSection> */}

        <HomeSection
          bg="bg-gradient-to-b from-sky-700 to-sky-200"
          slantBefore="up"
          className="absolute bottom-0"
        >
          <FooterSection />
        </HomeSection>
      </main>
    </>
  );
};

export default HomePage;
