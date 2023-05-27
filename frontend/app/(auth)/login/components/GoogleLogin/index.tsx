import Button from "@/app/components/ui/Button";
import Toast from "@/app/components/ui/Toast";
import { useGoogleLogin } from "./hooks/useGoogleLogin";

export const GoogleLoginButton = () => {
  const { isPending, messageToast, signInWithGoogle } = useGoogleLogin();

  return (
    <>
      <Button
        onClick={signInWithGoogle}
        isLoading={isPending}
        variant={"secondary"}
        type="button"
      >
        Login with Google
      </Button>
      <Toast ref={messageToast} />
    </>
  );
};
