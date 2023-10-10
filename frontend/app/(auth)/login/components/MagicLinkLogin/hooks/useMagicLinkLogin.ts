import { useState } from "react";

type UseMagicLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

export const useMagicLinkLogin = ({
  email,
  setEmail,
}: UseMagicLinkLoginProps): {
  handleMagicLinkLogin: () => Promise<void>;
  isPending: boolean;
} => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);

  const { publish } = useToast();

  const handleMagicLinkLogin = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: "Please enter your email address",
      });

      return;
    }

    setIsPending(true);

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: window.location.hostname, // current domain name. for eg localhost:3000, localhost:3001, https://...
      },
    });

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });
    } else {
      publish({
        variant: "success",
        text: "Magic link sent successfully if email recognized",
      });

      setEmail("");
    }
    setIsPending(false);
  };

  return { handleMagicLinkLogin, isPending };
};
