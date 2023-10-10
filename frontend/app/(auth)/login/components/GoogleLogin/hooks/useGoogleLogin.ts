import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks/useToast";

export const useGoogleLogin = (): {
  signInWithGoogle: () => Promise<void>;
  isPending: boolean;
} => {
  const { supabase } = useSupabase();

  const { publish } = useToast();

  const [isPending, setIsPending] = useState(false);

  const signInWithGoogle = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        queryParams: {
          access_type: "offline",
          prompt: "consent",
        },
      },
    });
    setIsPending(false);
    if (error) {
      publish({
        variant: "danger",
        text: "An error occurred ",
      });
    }
  };

  return {
    signInWithGoogle,
    isPending,
  };
};
