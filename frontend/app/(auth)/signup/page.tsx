"use client";
import Button from "@/app/components/ui/Button";
import Card from "@/app/components/ui/Card";
import Field from "@/app/components/ui/Field";
import PageHeading from "@/app/components/ui/PageHeading";
import Toast, { ToastRef } from "@/app/components/ui/Toast";
import { useSupabase } from "@/app/supabase-provider";
import { useRef, useState } from "react";

export default function SignUp() {
  const { supabase } = useSupabase();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPending, setIsPending] = useState(false);

  const signupToast = useRef<ToastRef>(null);

  const handleSignUp = async () => {
    setIsPending(true);
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
    });

    if (error) {
      console.error("Error signing up:", error.message);
      signupToast.current?.publish({
        variant: "danger",
        text: `Error signing up: ${error.message}`,
      });
    } else if (data) {
      console.log("User signed up");
      signupToast.current?.publish({ variant: "success", text: "Sign" });
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
              required
              type="email"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <Field
              name="password"
              required
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
        <h1 className="font-bold">Confirmation Email sent</h1>
        <p className="text-sm">Check your email.</p>
      </Toast>
      <Toast variant="danger" ref={signupToast} />
    </main>
  );
}
