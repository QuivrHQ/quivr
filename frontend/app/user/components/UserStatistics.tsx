/* eslint-disable */
"use client";
import Link from "next/link";
import prettyBytes from "pretty-bytes";
import { HTMLAttributes } from "react";

import Button from "@/lib/components/ui/Button";
import { UserStats } from "@/lib/types/User";
import { cn } from "@/lib/utils";

import { ApiKeyConfig } from "./ApiKeyConfig";
import { BrainConsumption } from "./BrainConsumption";
import { DateComponent } from "./Date";
import BrainSpaceChart from "./Graphs/BrainSpaceChart";
import { RequestsPerDayChart } from "./Graphs/RequestsPerDayChart";

export const UserStatistics = (userStats: UserStats): JSX.Element => {
  const { email, current_brain_size, max_brain_size, date, requests_stats } =
    userStats;

  return (
    <>
      <div className="flex flex-col sm:flex-row sm:items-center py-10 gap-5">
        <div className="flex-1 flex flex-col">
          <h1 className="text-4xl font-semibold">
            {email.split("@")[0] + "'"}s Brain Usage
          </h1>
          <p className="opacity-50">{email}</p>
          <Link className="mt-2" href={"/logout"}>
            <Button className="px-3 py-2" variant={"danger"}>
              Logout
            </Button>
          </Link>
        </div>

        <BrainConsumption {...userStats} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <UserStatisticsCard className="">
          <div>
            <h1 className="text-2xl font-semibold">
              {/* The last element corresponds to today's request_count */}
              Today{"'"}s Requests: {requests_stats.at(-1)?.requests_count}
            </h1>
            <DateComponent date={date} />
          </div>
          <div className="">
            <RequestsPerDayChart {...userStats} />
          </div>
        </UserStatisticsCard>

        <UserStatisticsCard>
          <div>
            <h1 className="text-2xl font-semibold">Remaining Brain size</h1>
            <p>
              {/* How much brain space is left */}
              {prettyBytes(max_brain_size - current_brain_size, {
                binary: true,
              })}
              /{prettyBytes(max_brain_size - 0, { binary: true })}
            </p>
          </div>
          <div className="">
            <BrainSpaceChart
              current_brain_size={current_brain_size}
              max_brain_size={max_brain_size}
            />
          </div>
        </UserStatisticsCard>
      </div>
      <ApiKeyConfig />
    </>
  );
};

const UserStatisticsCard = ({
  children,
  className,
}: HTMLAttributes<HTMLDivElement>) => {
  return (
    <div className={cn("w-full h-full flex flex-col gap-5", className)}>
      {children}
    </div>
  );
};

export default UserStatistics;
