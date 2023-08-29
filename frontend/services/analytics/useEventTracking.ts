"use client";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useJune } from "./useJune";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useEventTracking = () => {
  const analytics = useJune();
  const { session } = useSupabase();

  const track = async (
    event: string,
    properties?: Record<string, unknown>
  ): Promise<void> => {
    console.log("Event to track", event);
    if (analytics === undefined) {
      console.log("No analytics found");

      return;
    }
    await analytics.identify(session?.user.id, { email: session?.user.email });
    await analytics.track(event, properties);
  };

  return {
    track,
  };
};
