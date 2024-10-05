import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks/useToast";

export const useAzureLogin = (): {
  signInWithAzure: () => Promise<void>;
  isPending: boolean;
} => {
  const { supabase } = useSupabase();
  const { publish } = useToast();
  const [isPending, setIsPending] = useState(false);

  const signInWithAzure = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "azure",
      options: {
        scopes: "email",
      },
    });
    setIsPending(false);
    if (error) {
      publish({
        variant: "danger",
        text: "An error occurred during Azure login",
      });
    }
  };

  return {
    signInWithAzure,
    isPending,
  };
};
