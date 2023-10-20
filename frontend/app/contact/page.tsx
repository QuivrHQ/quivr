"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { redirect } from "next/navigation";

import Card from "@/lib/components/ui/Card";

import { ContactForm } from "./components";
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

      <main className="relative flex flex-col items-center px-10">
        <h1 className="text-4xl font-semibold my-10 text-center">
          Speak to our <span className="text-primary">Sales team</span>
        </h1>
        <Card className="flex flex-col items-center my-2 p-10 w-full max-w-xl">
          <ContactForm />
        </Card>
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
