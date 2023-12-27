"use client";
import { useTranslation } from "react-i18next";

import { StripePricingTable } from "@/lib/components/Stripe/PricingModal/components/PricingTable/PricingTable";
import Card from "@/lib/components/ui/Card";

import {
  FooterSection,
  HomeHeader,
  HomeSection,
  TestimonialsSection,
} from "../(home)/components";
import { UseCases } from "../(home)/components/UseCases/UseCases";

const ContactSalesPage = (): JSX.Element => {
  const { t } = useTranslation("contact");

  return (
    <div className="bg-[#FCFAF6]">
      <HomeHeader color="black" />

      <main className="relative flex flex-col items-center px-10">
        <h1 className="text-4xl font-semibold my-10 text-center">
          <span className="text-primary">{t("pricing")}</span>
        </h1>
        <Card className="my-auto flex flex-col h-fit mt-5 mb-10 p-10 w-full ">
          <StripePricingTable />
        </Card>
        <HomeSection
          bg="bg-[#362469]"
        >
          <UseCases />
          <div />
        </HomeSection>
        <HomeSection bg="bg-[#FCFAF6] ">
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
