import { useToast } from "@/app/hooks/useToast";
import { useSupabase } from "@/app/supabase-provider";
import { useState } from "react";

export const useGoogleLogin = () => {
  const { supabase } = useSupabase();

  const { setMessage, messageToast } = useToast();
  const [isPending, setIsPending] = useState(false);
  const signInWithGoogle = async () => {
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
      setMessage({
        type: "error",
        text: "An error occurred ",
      });
    }
  };

  return {
    signInWithGoogle,
    isPending,
    messageToast,
  };
};
