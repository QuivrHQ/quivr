/* eslint-disable */
"use client";
import { format, subDays } from "date-fns";
import {
  VictoryAxis,
  VictoryChart,
  VictoryChartProps,
  VictoryContainer,
  VictoryLine,
  VictoryTheme,
} from "victory";

type RequestStat = {
  date: string;
  daily_requests_count: number;
  user_id: string;
};

interface RequestsPerDayChartProps extends VictoryChartProps {
  requests_stats: RequestStat[];
}

export const RequestsPerDayChart = ({
  requests_stats,
  ...props
}: RequestsPerDayChartProps): JSX.Element => {
  const data = Array.from({ length: 7 }, (_, i) => subDays(new Date(), i))
    .map((date) => {
      const dateString = format(date, "yyyyMMdd");
      const stat = requests_stats.find((s) => s.date === dateString);

      return {
        date: format(date, "MM/dd/yyyy"),
        daily_requests_count: stat ? stat.daily_requests_count : 0,
      };
    })
    .reverse();

  return (
    <VictoryChart
      theme={VictoryTheme.material}
      containerComponent={
        <VictoryContainer
          className="bg-white dark:bg-black rounded-md w-full h-full"
          responsive={true}
        />
      }
      animate={{
        duration: 1000,
        onLoad: { duration: 1000 },
      }}
      {...props}
    >
      <VictoryAxis
        tickFormat={(tick) => {
          return `${tick.split("/")[0]}/${tick.split("/")[1]}`;
        }}
      />
      <VictoryAxis dependentAxis />
      <VictoryLine data={data} x="date" y="daily_requests_count" />
    </VictoryChart>
  );
};
