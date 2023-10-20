"use client";
import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { redirect } from "next/navigation";

const ContactSalesPage = (): JSX.Element => {
  const isNewHomePage = useFeatureIsOn("new-homepage-activated");
  if (!isNewHomePage) {
    redirect("/");
  }

  return <div>Not implemented</div>;
};

export default ContactSalesPage;
