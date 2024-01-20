import { useEffect } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToPreviousPageOrSearchPage } from "@/lib/helpers/redirectToPreviousPageOrSearchPage";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLogin = () => {
  const { session } = useSupabase();

  const { track } = useEventTracking();

  useEffect(() => {
    if (session?.user !== undefined) {
      void track("SIGNED_IN");
      redirectToPreviousPageOrSearchPage();
    }
  }, [session?.user]);
};
