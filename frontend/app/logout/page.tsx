"use client";
import { useEffect } from "react";
import Card from "../components/ui/Card";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";

export default function Logout() {
  const { supabase } = useSupabase();

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    
    if (error) {
      console.error("Error logging out:", error.message);
      alert(`Error logging out: ${error.message}`);
    } else {
      console.log("User logged out");
      alert("Logout successful!");
    }
  };

  useEffect(() => {
    handleLogout();
  }, []);

  return (
    <main>
      <section className="w-full outline-none pt-20 flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Logout" subtitle="See you next time"/>
        <Card className="w-1/2 flex justify-center items-center">
          <div className="text-center mt-2 p-6 max-w-sm w-full flex flex-col gap-5 items-center">
            <h1>You are now logged out.</h1>
          </div>
        </Card>
      </section>
    </main>
  );
}