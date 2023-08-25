"use client";
import { AnalyticsBrowser } from "@june-so/analytics-next";
import { useEffect, useState } from "react";

const juneApiKey = process.env.NEXT_PUBLIC_JUNE_API_KEY;

export const useJune = (): AnalyticsBrowser | undefined => {
  const [analytics, setAnalytics] = useState<AnalyticsBrowser | undefined>(
    undefined
  );

  useEffect(() => {
    const loadAnalytics = () => {
      if (juneApiKey === undefined) {
        console.log("No June API key found");

        return;
      }
      const response = AnalyticsBrowser.load({
        writeKey: juneApiKey,
      });
      console.log("Loaded June Analytics", response);
      setAnalytics(response);
    };
    loadAnalytics();
  }, []);

  return analytics;
};
