"use client";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useJune } from "./useJune";


// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useEventTracking = () => {
  const analytics = useJune();
  const { session } = useSupabase();

  const track = async (event: string): Promise<void> => {
    await analytics?.identify(session?.user.id, {email: session?.user.email});
    await analytics?.track(event);
  };

  return {
    track,
  };
};
