import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useToast } from "@/lib/hooks";

type UsePasswordForgottenProps = {
  email: string;
  setEmail: (email: string) => void;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePasswordForgotten = ({
  email,
  setEmail,
}: UsePasswordForgottenProps) => {
  const [isPending, setIsPending] = useState(false);
  const { supabase } = useSupabase();

  const { publish } = useToast();

  const handleRecoverPassword = async () => {
    if (email === "") {
      publish({
        variant: "danger",
        text: "Please enter your email address",
      });

      return;
    }

    setIsPending(true);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/recover-password`,
    });

    if (error) {
      publish({
        variant: "danger",
        text: error.message,
      });
    } else {
      publish({
        variant: "success",
        text: "Recovery mail will be sent if email recognized",
      });

      setEmail("");
    }
    setIsPending(false);
  };

  return {
    isPending,
    handleRecoverPassword,
  };
};
