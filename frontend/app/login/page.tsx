"use client";
import { useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";

export default function Login() {
  const { supabase } = useSupabase();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = async () => {
    await supabase.auth.signUp({
      email: email,
      password: password,
    });
  };

  const handleLogin = async () => {
    await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <main>
      <PageHeading title="Login" subtitle="Sign up, Login, or Logout" />
      <section className="w-full outline-none pt-20 flex flex-col gap-5 items-center justify-center p-6">
        <Card className="w-1/2">
          <div className="text-center mt-2 p-6 max-w-sm w-full flex flex-col gap-5 items-center">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              className="text-center"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="text-center"
            />
            <div className="flex justify-center gap-3">
              <Button onClick={handleSignUp}>Sign Up</Button>
              <Button onClick={handleLogin}>Login</Button>
              <Button onClick={handleLogout}>Logout</Button>
            </div>
            <div> Display token {}</div>
          </div>
        </Card>
      </section>
    </main>
  );
}
