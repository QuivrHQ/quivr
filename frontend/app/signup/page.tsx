"use client";
import { useRef, useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";
import Field from "../components/ui/Field";
import Toast, { ToastRef } from "../components/ui/Toast";

export default function SignUp() {
  const { supabase } = useSupabase();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPending, setIsPending] = useState(false);

  const signupToast = useRef<ToastRef>(null);
  const signupErrorToast = useRef<ToastRef>(null);
  const [error, setError] = useState("Unknown Error");

  const handleSignUp = async () => {
    setIsPending(true);
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
    });

    if (error) {
      console.error("Error signing up:", error.message);
      setError(error.message);
      signupErrorToast.current?.publish();
    } else if (data) {
      console.log("User signed up");
      signupToast.current?.publish();
    }
    setIsPending(false);
  };

  return (
    <main>
      <section className="w-full min-h-screen h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Sign Up" subtitle="Create your account" />
        <Card className="max-w-md w-full p-5 sm:p-10 text-left">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSignUp();
            }}
            className="flex flex-col gap-2"
          >
            <Field
              name="email"
              type="email"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <Field
              name="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
            <div className="flex flex-col items-center justify-center mt-2 gap-2">
              <Button isLoading={isPending}>Sign Up</Button>
            </div>
          </form>
        </Card>
      </section>
      <Toast variant="success" ref={signupToast}>
        Confirmation Email sent
      </Toast>
      <Toast variant="danger" ref={signupErrorToast}>
        {error}
      </Toast>
    </main>
  );
}
