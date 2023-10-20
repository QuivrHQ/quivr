"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { redirect } from "next/navigation";

import { HomeHeader } from "../(home)/components";

const ContactSalesPage = (): JSX.Element => {
  const isNewHomePage = useFeatureIsOn("new-homepage-activated");
  if (!isNewHomePage) {
    redirect("/");
  }

  return (
    <div className="bg-[#FCFAF6]">
      <HomeHeader color="black" />
    </div>
  );
};

export default ContactSalesPage;
