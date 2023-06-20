"use client"
import type { FeatureDefinition } from "@growthbook/growthbook";
import { GrowthBook, GrowthBookProvider } from "@growthbook/growthbook-react";
import axios from "axios";
import { useAsync } from "react-use";


const growthBook = new GrowthBook({
  apiHost: "https://cdn.growthbook.io",
  clientKey:process.env.NEXT_PUBLIC_GROWTHBOOK_CLIENT_KEY,
  enableDevMode: true,
});



const unauthenticatedClient = axios.create();

export const FeatureFlagsProvider = ({
  children,
}: {
  children?: React.ReactNode;
  }): JSX.Element => {

  const growthBookUrl = process.env.NEXT_PUBLIC_GROWTHBOOK_URL;
  
  useAsync(async () => {
    if (growthBookUrl !== undefined) {
      const growthBookInitResponse = await unauthenticatedClient.get<{
        features: Record<string, FeatureDefinition>;
      }>(growthBookUrl);
      growthBook.setFeatures(growthBookInitResponse.data.features);
    }
  });

  return (
    <GrowthBookProvider growthbook={growthBook}>{children}</GrowthBookProvider>
  );
};
