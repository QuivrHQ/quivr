import {
  CategoryScale,
  ChartDataset,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  ScriptableContext,
  Title,
  Tooltip,
} from "chart.js";
import { useLayoutEffect, useState } from "react";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  Filler,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

import { formatMinimalBrainsToSelectComponentInput } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/utils/formatMinimalBrainsToSelectComponentInput";
import { useAnalytics } from "@/lib/api/analytics/useAnalyticsApi";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const Analytics = (): JSX.Element => {
  const { getBrainsUsages } = useAnalytics();
  const { allBrains } = useBrainContext();
  const [chartData, setChartData] = useState({
    labels: [] as Date[],
    datasets: [{}] as ChartDataset<"line", number[]>[],
  });

  const graphRangeOptions = [
    { label: "Last 7 days", value: "Last 7 days" },
    { label: "Last 30 days", value: "Last 30 days" },
    { label: "Last 90 days", value: "Last 90 days" },
  ];

  const brainsWithUploadRights =
    formatMinimalBrainsToSelectComponentInput(allBrains);

  useLayoutEffect(() => {
    void (async () => {
      try {
        const res = await getBrainsUsages();
        const chartLabels = res?.usages.map((usage) => usage.date) as Date[];
        const chartDataset = res?.usages.map(
          (usage) => usage.usage_count
        ) as number[];

        setChartData({
          labels: chartLabels,
          datasets: [
            {
              label: "Usage Count",
              data: chartDataset,
              borderColor: "rgb(75, 192, 192)",
              backgroundColor: (context: ScriptableContext<"line">) => {
                const ctx = context.chart.ctx;
                const gradient = ctx.createLinearGradient(100, 100, 100, 250);
                gradient.addColorStop(0, "rgba(75, 192, 192, 0.4)");
                gradient.addColorStop(1, "rgba(75, 192, 192, 0.05)");

                return gradient;
              },
              fill: true,
            },
          ],
        });
      } catch (error) {
        console.error(error);
      }
    })();
  }, [chartData.labels.length]);

  const options = {
    type: "line",
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          display: false,
        },
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div>
      {chartData.labels.length ? (
        <div>
          <div>
            <SingleSelector
              iconName="calendar"
              options={graphRangeOptions}
              onChange={() => console.info("hey")}
              selectedOption={graphRangeOptions[0]}
              placeholder="Select range"
            />
            <SingleSelector
              iconName="brain"
              options={brainsWithUploadRights}
              onChange={() => console.info("hey")}
              selectedOption={undefined}
              placeholder="Select specific brain"
            />
          </div>
          <Line data={chartData} options={options} />
        </div>
      ) : (
        <LoaderIcon size="big" color="accent" />
      )}
    </div>
  );
};
