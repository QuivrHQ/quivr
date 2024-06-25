import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks/useToast";

export const useGithubLogin = (): {
  signInWithGithub: () => Promise<void>;
  isPending: boolean;
} => {
  const { supabase } = useSupabase();

  const { publish } = useToast();

  const [isPending, setIsPending] = useState(false);

  const signInWithGithub = async () => {
    setIsPending(true);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "github",
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
    signInWithGithub,
    isPending,
  };
};
