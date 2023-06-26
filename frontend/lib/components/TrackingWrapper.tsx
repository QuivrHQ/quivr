"use client";
import { usePageTracking } from "@/services/analytics/usePageTracking";

export const TrackingWrapper = (): JSX.Element => {
  usePageTracking();

  return <></>;
};
