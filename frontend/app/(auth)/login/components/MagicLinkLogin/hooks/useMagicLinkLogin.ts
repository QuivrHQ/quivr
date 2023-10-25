import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

type UseMagicLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const useMagicLinkLogin = ({
  email,
  setEmail,
}: UseMagicLinkLoginProps): {
  handleMagicLinkLogin: () => Promise<void>;
  isPending: boolean;
} => {
  const { supabase } = useSupabase();
  const [isPending, setIsPending] = useState(false);
  const { t } = useTranslation("login");
  const { publish } = useToast();

  const handleMagicLinkLogin = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: t("errorMailMissed"),
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
