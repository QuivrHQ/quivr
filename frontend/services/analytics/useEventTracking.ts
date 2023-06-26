"use client";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useJune } from "./useJune";

type TrackedEvent = "SIGNED_IN";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useEventTracking = () => {
  const analytics = useJune();
  const { session } = useSupabase();

  const track = async (event: TrackedEvent): Promise<void> => {
    await analytics?.identify(session?.user.id);
    await analytics?.track(event);
  };

  return {
    track,
  };
};
