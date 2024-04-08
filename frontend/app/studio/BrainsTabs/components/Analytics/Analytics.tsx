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

import { useAnalytics } from "@/lib/api/analytics/useAnalyticsApi";

export const Analytics = (): JSX.Element => {
  const { getBrainsUsages } = useAnalytics();

  const [chartData, setChartData] = useState({
    labels: [] as Date[],
    datasets: [{}] as ChartDataset<"line", number[]>[],
  });

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

      console.info(chartData);
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
      <h2>Analytics</h2>
      {chartData.labels.length ? (
        <Line data={chartData} options={options} />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};
