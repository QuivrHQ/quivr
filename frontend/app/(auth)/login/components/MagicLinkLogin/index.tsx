"use client";

import Button from "@/lib/components/ui/Button";

import { useMagicLinkLogin } from "./hooks/useMagicLinkLogin";

type MaginLinkLoginProps = {
  email: string;
  setEmail: (email: string) => void;
};

export const MagicLinkLogin = ({
  email,
  setEmail,
}: MaginLinkLoginProps): JSX.Element => {
  const { handleMagicLinkLogin, isPending } = useMagicLinkLogin({
    email,
    setEmail,
  });

  return (
    <Button
      type="button"
      variant={"tertiary"}
      onClick={() => void handleMagicLinkLogin()}
      isLoading={isPending}
    >
      Send Magic Link
    </Button>
  );
};
