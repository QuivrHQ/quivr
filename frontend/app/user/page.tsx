"use client";
import axios from "axios";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { useSupabase } from "../supabase-provider";
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
            <div>
              <h2>Email: {userStats.email}</h2>
              <h2>Max Brain Size: {userStats.max_brain_size}</h2>
              <h2>Current Brain Size: {userStats.current_brain_size}</h2>
              {/* <h2>Max Requests Number: {userStats.max_requests_number}</h2>
            <h2>Requests Stats: {userStats.requests_stats}</h2> */}
              <h2>Date: {userStats.date}</h2>
            </div>
          )}
        </div>
      </main>
    </>
  );
}
