"use client";
import axios from "axios";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import Card from "../components/ui/Card";
import { useSupabase } from "../supabase-provider";
import { UserStatistics } from "./components";
import { UserStats } from "./types";

export default function UserPage() {
  const [userStats, setUserStats] = useState<UserStats>();
  const { session } = useSupabase();
  if (session === null) {
    redirect("/login");
  }

  useEffect(() => {
    const fetchUserStats = async () => {
      // setIsPending(true);
      try {
        console.log(
          `Fetching user stats from ${process.env.NEXT_PUBLIC_BACKEND_URL}/user`
        );
        const response = await axios.get<UserStats>(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/user`,
          {
            headers: {
              Authorization: `Bearer ${session.access_token}`,
            },
          }
        );
        setUserStats(response.data);
      } catch (error) {
        console.error("Error fetching user stats", error);
        setUserStats(undefined);
      }
    };
    fetchUserStats();
  }, [session.access_token]);

  return (
    <main className="w-full flex flex-col pt-32">
      <section className="flex flex-col justify-center items-center flex-1 gap-5 h-full">
        <Card className="p-5 max-w-3xl w-full min-h-full flex-1 mb-24">
          {userStats && (
            <>
              <UserStatistics {...userStats} />
            </>
          )}
        </Card>
      </section>
    </main>
  );
}
