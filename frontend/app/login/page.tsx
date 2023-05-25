"use client";
import { useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";
import { redirect } from "next/navigation";
import Link from "next/link";
import Field from "../components/ui/Field";

export default function Login() {
  const { supabase } = useSupabase();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });

    if (error) {
      console.error("Error logging in:", error.message);
      alert(`Error logging in: ${error.message}`);
    } else if (data) {
      console.log("User logged in:", data);
      alert("Login successful!");
    }
  };

  return (
    <main>
      <section className="w-full min-h-screen h-full outline-none flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Login" subtitle="Welcome back" />
        <Card className="max-w-md w-full flex flex-col p-5 sm:p-10 gap-2 text-left">
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
            <Button onClick={handleLogin}>Login</Button>
            <Link href="/signup">Dont have an account? Sign up</Link>
          </div>
        </Card>
      </section>
    </main>
  );
}
