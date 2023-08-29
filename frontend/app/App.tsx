"use client";

import { PropsWithChildren, useEffect } from "react";

import Footer from "@/lib/components/Footer";
import { NavBar } from "@/lib/components/NavBar";
import { TrackingWrapper } from "@/lib/components/TrackingWrapper";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { UpdateMetadata } from "@/lib/helpers/updateMetadata";
import "../lib/config/LocaleConfig/i18n";

// This wrapper is used to make effect calls at a high level in app rendering.
export const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { fetchAllBrains, fetchAndSetActiveBrain, fetchPublicPrompts } =
    useBrainContext();
  const { session } = useSupabase();

  useEffect(() => {
    void fetchAllBrains();
    void fetchAndSetActiveBrain();
    void fetchPublicPrompts();
  }, [session?.user]);

  return (
    <>
      <TrackingWrapper />
      <NavBar />
      <div className="flex-1">{children}</div>
      <Footer />
      <UpdateMetadata />
    </>
  );
};
