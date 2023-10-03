"use client";
import prettyBytes from "pretty-bytes";
import { useTranslation } from "react-i18next";

import Card, { CardBody, CardHeader } from "@/lib/components/ui/Card";
import Spinner from "@/lib/components/ui/Spinner";
import { useUserData } from "@/lib/hooks/useUserData";
import { UserStats } from "@/lib/types/User";

import { BrainConsumption } from "./BrainConsumption";
import { DateComponent } from "./Date";
import BrainSpaceChart from "./Graphs/BrainSpaceChart";
import { RequestsPerDayChart } from "./Graphs/RequestsPerDayChart";

export const formatBrainSizeUsage = (
  currentBrainSize: number,
  maxBrainSize: number
): string => {
  const sizeInUse = prettyBytes(maxBrainSize - currentBrainSize, {
    binary: true,
  });

  const totalSize = prettyBytes(maxBrainSize - 0, { binary: true });

  return `${sizeInUse} / ${totalSize}`;
};

export const UserStatistics = (): JSX.Element => {
  const { userData }: { userData?: UserStats } = useUserData();
  const { t } = useTranslation(["user"]);

  if (!userData) {
    return (
      <div className="flex items-center justify-center">
        <span>{t("fetching", { ns: "user" })}</span>
        <Spinner />
      </div>
    );
  }

  const { current_brain_size, max_brain_size, date, requests_stats } = userData;

  return (
    <div className="flex flex-col md:flex-row gap-2 w-full">
      <Card className="shadow-none hover:shadow-none w-full md:w-1/4 md:self-start">
        <CardHeader className="border-b-0">
          <h3 className="font-semibold">{t("brainUsage")}</h3>
        </CardHeader>
        <CardBody className="flex justify-center items-center">
          <BrainConsumption {...userData} />
        </CardBody>
      </Card>

      <div className="w-full md:w-3/4 flex flex-col md:flex-row gap-2">
        <Card className="shadow-none hover:shadow-none w-full md:w-1/2">
          <CardHeader className="border-b-0">
            <h3 className="font-semibold">
              {/* The last element corresponds to today's request_count */}
              {t("requestsCount", {
                count: requests_stats.at(-1)?.daily_requests_count,
              })}
            </h3>
            <p className="text-slate-500 font-light text-sm">
              <DateComponent date={date} />
            </p>
          </CardHeader>

          <CardBody>
            <RequestsPerDayChart {...userData} />
          </CardBody>
        </Card>

        <Card className="shadow-none hover:shadow-none w-full md:w-1/2">
          <CardHeader className="border-b-0">
            <h3 className="font-semibold">{t("brainSize")}</h3>
            <p className="text-slate-500 font-light text-sm">
              {formatBrainSizeUsage(current_brain_size, max_brain_size)}
            </p>
          </CardHeader>
          <CardBody>
            <BrainSpaceChart
              current_brain_size={current_brain_size}
              max_brain_size={max_brain_size}
            />
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default UserStatistics;
