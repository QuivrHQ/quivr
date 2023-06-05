import { format, subDays } from "date-fns";
import React from "react";
import {
  VictoryAxis,
  VictoryChart,
  VictoryContainer,
  VictoryLine,
  VictoryTheme,
} from "victory";

type RequestStat = {
  date: string;
  requests_count: number;
  user_id: string;
};

type RequestsPerDayChartProps = {
  requests_stats: RequestStat[];
};

export const RequestsPerDayChart: React.FC<RequestsPerDayChartProps> = ({
  requests_stats,
}) => {
  const data = Array.from({ length: 7 }, (_, i) => subDays(new Date(), i))
    .map((date) => {
      const dateString = format(date, "yyyyMMdd");
      const stat = requests_stats.find((s) => s.date === dateString);
      return {
        date: format(date, "MM/dd/yyyy"),
        requests_count: stat ? stat.requests_count : 0,
      };
    })
    .reverse();

  return (
    <VictoryChart
      domainPadding={20}
      theme={VictoryTheme.material}
      containerComponent={<VictoryContainer responsive={true} />}
    >
      <VictoryAxis
        tickFormat={(tick) => {
          return `${tick.split("/")[0]}/${tick.split("/")[1]}`;
        }}
      />
      <VictoryAxis dependentAxis />
      <VictoryLine data={data} x="date" y="requests_count" />
    </VictoryChart>
  );
};
