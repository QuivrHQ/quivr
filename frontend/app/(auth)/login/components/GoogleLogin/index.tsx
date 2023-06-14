/* eslint-disable */
import Button from "@/lib/components/ui/Button";

import { useGoogleLogin } from "./hooks/useGoogleLogin";

export const GoogleLoginButton = () => {
  const { isPending, signInWithGoogle } = useGoogleLogin();

  return (
    <Button
      onClick={signInWithGoogle}
      isLoading={isPending}
      variant={"secondary"}
      type="button"
    >
      Login with Google
    </Button>
  );
};
