/* eslint-disable */
"use client";

import Button from "@/lib/components/ui/Button";
import { usePasswordForgotten } from "./hooks/usePasswordForgotten";

type PasswordForgottenProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const PasswordForgotten = ({
  email,
  setEmail,
}: PasswordForgottenProps) => {
  const { isPending, handleRecoverPassword } = usePasswordForgotten({
    email,
    setEmail,
  });
  return (
    <Button
      type="button"
      variant={"tertiary"}
      onClick={handleRecoverPassword}
      isLoading={isPending}
    >
      Password forgotten
    </Button>
  );
};
