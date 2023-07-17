"use client";

import { PropsWithChildren, useEffect } from "react";

import Footer from "@/lib/components/Footer";
import { NavBar } from "@/lib/components/NavBar";
import { TrackingWrapper } from "@/lib/components/TrackingWrapper";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";

// This wrapper is used to make effect calls at a high level in app rendering.
export const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { fetchAllBrains, fetchAndSetActiveBrain } = useBrainContext();
  const { session } = useSupabase();

  useEffect(() => {
    void fetchAllBrains();
    void fetchAndSetActiveBrain();
  }, [session?.user]);

  return (
    <>
      <TrackingWrapper />
      <NavBar />
      <div className="flex-1">{children}</div>
      <Footer />
    </>
  );
};
