"use client";
import { StripePricingTable } from "@/lib/components/Stripe/PricingModal/components/PricingTable/PricingTable";

import {
  FooterSection,
  HomeHeader,
  HomeSection,
  TestimonialsSection,
} from "../(home)/components";
import { UseCases } from "../(home)/components/UseCases/UseCases";

const ContactSalesPage = (): JSX.Element => {
  return (
    <div className="bg-[#FCFAF6]">
      <HomeHeader color="black" />

      <main className="relative flex flex-col items-center px-10">
        <section className="flex flex-col h-fit mt-5 mb-10 p-10 w-full">
          <div className="rounded-xl overflow-hidden">
            <div className="p-8 text-center">
              <h1 className="text-6xl font-bold text-primary mb-4">Pricing</h1>
              <p className="text-2xl font-semibold text-gray-700 mb-6">
                Explore our extensive free tier, or upgrade for more features.
              </p>
            </div>

            {/* Stripe Pricing Table */}

            <StripePricingTable />
          </div>
        </section>

        <HomeSection bg="bg-[#362469]">
          <UseCases />
          <div />
        </HomeSection>

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
