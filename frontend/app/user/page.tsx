"use client";
import axios from "axios";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { useSupabase } from "../supabase-provider";
import { UserStatistics } from "./components";
import { UserStats } from "./types";

export default function UserPage() {
  // need to fetch everything with a user effect
  const [userStats, setUserStats] = useState<UserStats>();
  // const [isPending, setIsPending] = useState(true);
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
      // setIsPending(false);
    };
    fetchUserStats();
  }, [session.access_token]);

  return (
    <>
      <main className="pt-24">
        <div>
          {userStats && (
            <>
              <UserStatistics {...userStats} />
            </>
          )}
        </div>
      </main>
    </>
  );
}
