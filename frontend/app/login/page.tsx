"use client";

import { useSupabase } from "../supabase-provider";

export default function Login() {
  const { supabase } = useSupabase();

  const handleSignUp = async () => {
    await supabase.auth.signUp({
      email: "girard.stanislas@gmail.com",
      password: "sup3rs3cur3",
    });
  };

  const handleLogin = async () => {
    await supabase.auth.signInWithPassword({
      email: "girard.stanislas@gmail.com",
      password: "sup3rs3cur3",
    });
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <main>
        <section  className="w-full outline-none pt-20 flex flex-col gap-5 items-center justify-center p-6">
      <button onClick={handleSignUp}>Sign Up</button>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
      <div> Display token {}</div>
      </section>
    </main>
  );
}