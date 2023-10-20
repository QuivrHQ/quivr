"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { redirect } from "next/navigation";

import {
  FooterSection,
  HomeHeader,
  HomeSection,
  TestimonialsSection,
} from "../(home)/components";

const ContactSalesPage = (): JSX.Element => {
  const isNewHomePage = useFeatureIsOn("new-homepage-activated");
  if (!isNewHomePage) {
    redirect("/");
  }

  return (
    <div className="bg-[#FCFAF6]">
      <HomeHeader color="black" />

      <main className="relative flex flex-col items-center">
        TODO: The Form!
        <HomeSection bg="bg-[#FCFAF6]">
          <TestimonialsSection />
        </HomeSection>
        <HomeSection bg="bg-gradient-to-b from-[#D07DF9] to-[#7A27FD]">
          <FooterSection />
        </HomeSection>
      </main>
    </div>
  );
};

export default ContactSalesPage;
