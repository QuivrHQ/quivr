"use client";

import { PropsWithChildren, useEffect } from "react";

import Footer from "@/lib/components/Footer";
import { NavBar } from "@/lib/components/NavBar";
import { TrackingWrapper } from "@/lib/components/TrackingWrapper";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

// This wrapper is used to make effect calls at a high level in app rendering.
export const App = ({ children }: PropsWithChildren): JSX.Element => {
  const { fetchAllBrains, fetchAndSetActiveBrain } = useBrainContext();

  useEffect(() => {
    void fetchAllBrains();
    void fetchAndSetActiveBrain();
  }, []);

  return (
    <>
      <TrackingWrapper />
      <NavBar />
      <div className="flex-1">{children}</div>
      <Footer />
    </>
  );
};
